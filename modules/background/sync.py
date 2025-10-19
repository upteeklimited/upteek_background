import time
import datetime
from sqlalchemy import MetaData, Table, select
from database.redis import redis_client
from database.db import engine, shadow_engine, SessionLocal, ShadowSessionLocal, get_laravel_datetime, main_meta, shadow_meta
from models.sync_logs import SyncLog, create_sync_log, update_sync_log_by_table_name, get_single_sycn_log_by_table_name

# def get_last_sync_time(hours: int=24):
# 	last_sync = redis_client.get("last_sync_timestamp")
# 	if last_sync:
# 		return datetime.datetime.fromisoformat(last_sync)
# 	return datetime.datetime.utcnow() - datetime.timedelta(hours=hours)

# def update_last_sync_time():
# 	now = datetime.datetime.utcnow().isoformat()
# 	redis_client.set("last_sync_timestamp", now)

def get_last_sync_time(db, table_name):
	log = get_single_sycn_log_by_table_name(db=db, table_name=table_name)
	if log:
		return log.last_synced_at
	else:
		log = create_sync_log(db=db, table_name=table_name, last_synced_at=get_laravel_datetime(), commit=True)
		return log.last_synced_at

def update_sync_time(db, table_name):
	log = get_single_sycn_log_by_table_name(db=db, table_name=table_name)
	if log:
		update_sync_log_by_table_name(db=db, table_name=table_name, values={'last_synced_at': get_laravel_datetime()}, commit=True)
	return True

def get_all_table_names(engine):
	metadata = MetaData()
	metadata.reflect(bind=engine)
	return list(metadata.tables.keys())

def get_all_tables():
	global engine
	metadata = MetaData()
	metadata.reflect(bind=engine)
	return list(metadata.tables.keys())

def sync_table(table_name):
	global engine, shadow_engine
	main_db = SessionLocal()
	shadow_db = ShadowSessionLocal()

	try:
		main_table = Table(table_name, main_meta, autoload_with=engine)
		shadow_table = Table(table_name, shadow_meta, autoload_with=shadow_engine)

		count_stmt = select(func.count()).select_from(shadow_table)
		shadow_count = shadow_db.execute(count_stmt).scalar_one()

		if shadow_count == 0:
			print(f"Shadow table '{table_name}' is empty — performing full copy...")
			all_rows = main_db.execute(select(main_table)).mappings().all()

			if all_rows:
				shadow_db.execute(shadow_table.insert(), all_rows)
				shadow_db.commit()
				print(f"Copied {len(all_rows)} rows to shadow table '{table_name}'.")

			update_sync_time(shadow_db, table_name)
			update_sync_time(main_db, table_name)
			return

		last_sync = get_last_sync_time(shadow_db, table_name)

		stmt = select(main_table).where(main_table.c.updated_at > last_sync)
		updated_rows = main_db.execute(stmt).fetchall()

		for row in updated_rows:
			values = dict(row._mapping)
			pk = list(main_table.primary_key.columns)[0].name
			pk_value = values[pk]

			# Try to update, else insert
			result = shadow_db.execute(
			shadow_table.update().where(shadow_table.c[pk] == pk_value).values(**values)
			)
			if result.rowcount == 0:
				shadow_db.execute(shadow_table.insert().values(**values))
		
		# Handle HARD DELETES (rows that exist in shadow but not in main)
		main_ids = [r[0] for r in main_db.execute(select(main_table.c.id)).fetchall()]
		shadow_ids = [r[0] for r in shadow_db.execute(select(shadow_table.c.id)).fetchall()]
		ids_to_delete = set(shadow_ids) - set(main_ids)
		if ids_to_delete:
			shadow_db.execute(shadow_table.delete().where(shadow_table.c.id.in_(ids_to_delete)))

		shadow_db.commit()
		update_sync_time(shadow_db, table_name)
		update_sync_time(main_db, table_name)

	except Exception as e:
		shadow_db.rollback()
		print(f"Error syncing {table_name}: {e}")
	finally:
		main_db.close()
		shadow_db.close()


def sync_databases():
	main_session = SessionLocal()
	shadow_session = ShadowSessionLocal()

	try:
		last_sync = get_last_sync_time()
		now = datetime.datetime.utcnow()

		print(f"Starting sync from {last_sync} to {now}")

		metadata_main = MetaData()
		metadata_main.reflect(bind=engine)
		metadata_shadow = MetaData()
		metadata_shadow.reflect(bind=shadow_engine)

		TABLES = get_all_tables()
		print(f"Found tables: {TABLES}")

		for table_name in TABLES:
			print(f"\nSyncing table: {table_name}")

			main_table = Table(table_name, metadata_main, autoload_with=engine)
			shadow_table = Table(table_name, metadata_shadow, autoload_with=shadow_engine)
			pk = list(main_table.primary_key.columns)[0]

			# --- 0. Check if shadow table is empty ---
			shadow_count = shadow_session.execute(
                select(func.count()).select_from(shadow_table)
            ).scalar()

			if shadow_count == 0:
				print(f"Shadow table '{table_name}' is empty. Performing full copy...")
				rows = main_session.execute(select(main_table)).mappings().all()
				if rows:
					shadow_session.execute(shadow_table.insert(), rows)
					shadow_session.commit()
					print(f"✅ Full copy completed for '{table_name}' ({len(rows)} rows).")
				else:
					print(f"⚠️ No data found in main table '{table_name}'. Skipping.")
				continue

			# --- 1. Fetch recently updated/inserted records ---
			stmt = select(main_table).where(main_table.c.updated_at > last_sync)
			updated_rows = main_session.execute(stmt).mappings().all()

			for row in updated_rows:
				# Check if row exists in shadow
				shadow_row = shadow_session.execute(
                    select(shadow_table).where(getattr(shadow_table.c, pk.name) == row[pk.name])
                ).first()

				if shadow_row:
					# Update
					shadow_session.execute(
						shadow_table.update()
						.where(getattr(shadow_table.c, pk.name) == row[pk.name])
						.values(**row)
					)
				else:
					# Insert
					shadow_session.execute(shadow_table.insert().values(**row))

				# --- 2. Handle deletions ---
			if "deleted_at" in main_table.c:
				deleted_stmt = select(main_table.c[pk.name]).where(
					main_table.c.deleted_at > last_sync
				)
				deleted_ids = [r[0] for r in main_session.execute(deleted_stmt).all()]
				if deleted_ids:
					shadow_session.execute(
					    shadow_table.delete().where(
					        getattr(shadow_table.c, pk.name).in_(deleted_ids)
					    )
					)

			shadow_session.commit()

		update_last_sync_time()
		print("Sync complete.")

	except Exception as e:
		shadow_session.rollback()
		print(f"Sync failed: {e}")
	finally:
		main_session.close()
		shadow_session.close()


def sync_all_tables():
	global engine
	TABLES = get_all_table_names(engine)
	for table in TABLES:
		if table != "sync_logs":
			print(f"Syncing table: {table}")
			sync_table(table)
		else:
			continue
	return True
