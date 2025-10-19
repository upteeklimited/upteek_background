from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, mapper
from settings.config import load_env_config
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from pathlib import Path
import os
import subprocess

config = load_env_config()

SQLALCHEMY_DATABASE_URL  = config['cleardb_database_url']
SQLALCHEMY_BACKUP_DATABASE_URL  = config['cleardb_backup_database_url']

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=60)
shadow_engine = create_engine(SQLALCHEMY_BACKUP_DATABASE_URL, pool_recycle=60)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=True)
ShadowSessionLocal = sessionmaker(bind=shadow_engine, autocommit=False, autoflush=True)

Base = declarative_base()

session = SessionLocal()
shadow_session = ShadowSessionLocal()

main_meta = MetaData()
main_meta.reflect(bind=engine)
shadow_meta = MetaData(bind=shadow_engine)
shadow_meta.reflect(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()

def get_laravel_datetime():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# def get_added_laravel_datetime(days=1):
#     begin = date.today()
#     end = begin + timedelta(days=days)
#     return end.strftime("%Y-%m-%d %H:%M:%S")
    
def get_added_laravel_datetime(days=1):
    begin = datetime.today()
    end = begin + timedelta(days=days)
    return str(int(end.timestamp()))

# def compare_laravel_datetime_with_today(datetime_str=None):
#     if datetime_str is None:
#         return False
#     else:
#         com_datetime_str = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
#         dnow = datetime.now()
#         if com_datetime_str.time() > dnow.time():
#             return True
#         else:
#             return False
            
def compare_laravel_datetime_with_today(datetime_str=None):
    if datetime_str is None:
        return False
    else:
        fu_ts = int(datetime_str)
        dnow = int(datetime.now().timestamp())
        if fu_ts > dnow:
            return True
        else:
            return False

def has_uncommitted_changes(db: Session) -> bool:
    return db.dirty or db.new or db.deleted

def is_object_modified(db: Session, obj) -> bool:
    return db.is_modified(obj)

def has_active_transaction(db: Session) -> bool:
    return db.in_transaction()


class DatabaseBackup:
    def __init__(self):
        self.backup_dir = Path(config['backup_dir'])
        self.backup_dir.mkdir(exist_ok=True)

    def create_backup(self, db_name: str, db_user: str, db_password: str, db_host: str = "localhost") -> str:
        """Create a database backup using mysqldump"""
        backup_file = self.backup_dir / f"backup_{db_name}_{timestamp}.sql"

        try:
            cmd = [
                "mysqldump", f"--user={db_user}",f"--password={db_password}", f"--host={db_host}", db_name
            ]

            with open(backup_file, 'w') as f:
                result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)

            if result.returncode != 0:
                raise Exception(f"mysqldump failed: {result.stderr}")

            return str(backup_file)
        except Exception as e:
            if backup_file.exists():
                backup_file.unlink()
            raise e

    def list_backups(self) -> list:
        return [f.name for f in self.backup_dir.glob("*.sql")]

    def restore_backup(self, backup_file: str, db_name: str, db_user: str, db_password: str, db_host: str = "localhost"):
        backup_path = self.backup_dir / backup_file

        if not backup_path.exists():
            raise FileNotFoundError(f"Backup file {backup_file} not found")

        cmd = [
            "mysql", f"--user={db_user}", f"--password={db_password}", f"--host={db_host}", db_name
        ]

        with open(backup_path, 'r') as f:
            result = subprocess.run(cmd, stdin=f, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            raise Exception(f"Restore failed: {result.stderr}")

