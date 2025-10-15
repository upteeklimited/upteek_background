from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Batch(Base):

    __tablename__ = "batches"
     
    id = Column(BigInteger, primary_key=True, index=True)
    current_job_id = Column(BigInteger, default=0)
    batch_type = Column(Integer, default=0)
    reference = Column(String, nullable=True)
    run_date = Column(String, nullable=True)
    failed_reason = Column(Text, nullable=True)
    status_string = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    started_at = Column(TIMESTAMP(timezone=True), nullable=True)
    ended_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_batch(db: Session, current_job_id: int = 0, batch_type: int = 0, reference: str = None, run_date: str = None, failed_reason: str = None, status_string: str = None, status: int = 0, started_at: str = None, ended_at: str = None, commit: bool=False):
    batch = Batch(current_job_id=current_job_id, batch_type=batch_type, reference=reference, run_date=run_date, failed_reason=failed_reason, status_string=status_string, status=status, started_at=started_at, ended_at=ended_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(batch)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(batch)
    return batch

def update_batch(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Batch).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_batch(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Batch).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_batch(db: Session, id: int=0, commit: bool=False):
    db.query(Batch).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_batch_by_id(db: Session, id: int=0):
    return db.query(Batch).filter_by(id = id).first()

def get_batches(db: Session, filters: Dict={}):
    query = db.query(Batch)
    if 'current_job_id' in filters:
        query = query.filter_by(current_job_id = filters['current_job_id'])
    if 'batch_type' in filters:
        query = query.filter_by(batch_type = filters['batch_type'])
    if 'reference' in filters:
        query = query.filter_by(reference = filters['reference'])
    return query.order_by(desc(Batch.created_at))
