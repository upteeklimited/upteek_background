from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class SyncLog(Base):

    __tablename__ = "sync_logs"
     
    id = Column(BigInteger, primary_key=True, index=True)
    table_name = Column(String, nullable=True)
    last_synced_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_sync_log(db: Session, table_name: str = None, last_synced_at: str = None, commit: bool=False):
    sync_log = SyncLog(table_name=table_name, last_synced_at=last_synced_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(sync_log)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(sync_log)
    return sync_log

def update_sync_log(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(SyncLog).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def update_sync_log_by_table_name(db: Session, table_name: str=None, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(SyncLog).filter_by(table_name = table_name).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_sync_log(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(SyncLog).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_sync_log(db: Session, id: int=0, commit: bool=False):
    db.query(SyncLog).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_sycn_log_by_id(db: Session, id: int=0):
    return db.query(SyncLog).filter_by(id = id).first()

def get_single_sycn_log_by_table_name(db: Session, table_name: str: None):
    return db.query(SyncLog).filter_by(table_name = table_name).first()

def get_sync_logs(db: Session, filters: Dict={}):
    query = db.query(SyncLog)
    if 'table_name' in filters:
        query = query.filter_by(table_name = filters['table_name'])
    return query.order_by(desc(SyncLog.created_at))
