import time
import datetime
from sqlalchemy import MetaData, Table, select
from database.redis import redis_client
from database.db import engine, shadow_engine, SessionLocal, ShadowSessionLocal

def get_last_sync_time(hours: int=24):
	last_sync = redis_client.get("last_sync_timestamp")
	if last_sync:
		return datetime.datetime.fromisoformat(last_sync)
	return datetime.datetime.utcnow() - datetime.timedelta(hours=hours)


def update_last_sync_time():
	now = datetime.datetime.utcnow().isoformat()
	redis_client.set("last_sync_timestamp", now)


def get_all_tables():
	metadata = MetaData()
	metadata.reflect(bind=engine)
	return list(metadata.tables.keys())

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

			# --- 1. Fetch recently updated/inserted records ---
			stmt = select(main_table).where(main_table.c.updated_at > last_sync)
			updated_rows = main_session.execute(stmt).mappings().all()

			for row in updated_rows:
				pk = list(main_table.primary_key.columns)[0]
				shadow_row = shadow_session.execute(
                    select(shadow_table).where(getattr(shadow_table.c, pk.name) == row[pk.name])
                ).first()

                if shadow_row:
                	shadow_session.execute(
                        shadow_table.update()
                        .where(getattr(shadow_table.c, pk.name) == row[pk.name])
                        .values(**row)
                    )
                else:
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

