from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Job(Base):

    __tablename__ = "jobs"
     
    id = Column(BigInteger, primary_key=True, index=True)
    batch_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    code = Column(String, nullable=True)
    failed_reason = Column(Text, nullable=True)
    status_string = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    started_at = Column(TIMESTAMP(timezone=True), nullable=True)
    ended_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_job(db: Session, batch_id: int = 0, name: str = None, code: str = None, failed_reason: str = None, status_string: str = None, status: int = 0, started_at: str = None, ended_at: str = None, commit: bool=False):
    job = Job(batch_id=batch_id, name=name, code=code, failed_reason=failed_reason, status_string=status_string, status=status, started_at=started_at, ended_at=ended_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(job)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(job)
    return job

def update_job(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Job).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_job(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Job).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_job(db: Session, id: int=0, commit: bool=False):
    db.query(Job).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_job_by_id(db: Session, id: int=0):
    return db.query(Job).filter_by(id = id).first()

def get_jobs(db: Session, filters: Dict={}):
    query = db.query(Job)
    if 'batch_id' in filters:
        query = query.filter_by(batch_id = filters['batch_id'])
    if 'code' in filters:
        query = query.filter_by(code = filters['code'])
    return query.order_by(desc(Job.created_at))
