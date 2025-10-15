from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Batch_Log(Base):

    __tablename__ = "batch_logs"
     
    id = Column(BigInteger, primary_key=True, index=True)
    batch_id = Column(BigInteger, default=0)
    job_id = Column(BigInteger, default=0)
    info = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    started_at = Column(TIMESTAMP(timezone=True), nullable=True)
    ended_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_batch_log(db: Session, batch_id: int = 0, job_id: int = 0, info: str = None, status: int = 0, started_at: str = None, ended_at: str = None, commit: bool=False):
    batch_log = Batch_Log(batch_id=batch_id, name=name, code=code, failed_reason=failed_reason, status_string=status_string, status=status, started_at=started_at, ended_at=ended_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(batch_log)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(batch_log)
    return batch_log

def update_batch_log(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Batch_Log).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_batch_log(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Batch_Log).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_batch_log(db: Session, id: int=0, commit: bool=False):
    db.query(Batch_Log).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_batch_log_by_id(db: Session, id: int=0):
    return db.query(Batch_Log).filter_by(id = id).first()

def get_batch_logs(db: Session, filters: Dict={}):
    query = db.query(Batch_Log)
    if 'batch_id' in filters:
        query = query.filter_by(batch_id = filters['batch_id'])
    if 'job_id' in filters:
        query = query.filter_by(job_id = filters['job_id'])
    return query.order_by(desc(Batch_Log.created_at))
