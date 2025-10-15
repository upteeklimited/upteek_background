from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class LoanApplicationLog(Base):

    __tablename__ = "loan_application_logs"
     
    id = Column(BigInteger, primary_key=True, index=True)
    application_id = Column(BigInteger, default=0)
    approved_user_id = Column(BigInteger, default=0)
    rejected_user_id = Column(BigInteger, default=0)
    approval_level = Column(Integer, default=0)
    decline_reason = Column(Text, nullable=True)
    is_top_up = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    approved_at = Column(TIMESTAMP(timezone=True), nullable=True)
    rejected_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_loan_application_log(db: Session, application_id: int = 0, approved_user_id: int = 0, rejected_user_id: int = 0, approval_level: int = 0, decline_reason: str = None, is_top_up: int = 0, status: int = 0, approved_at: str = None, rejected_at: str = None, commit: bool=False):
    la_log = LoanApplicationLog(application_id=application_id, approved_user_id=approved_user_id, rejected_user_id=rejected_user_id, approval_level=approval_level, decline_reason=decline_reason, is_top_up=is_top_up, status=status, approved_at=approved_at, rejected_at=rejected_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(la_log)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(la_log)
    return la_log

def update_loan_application_log(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(LoanApplicationLog).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_loan_application_log(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(LoanApplicationLog).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_loan_application_log(db: Session, id: int=0, commit: bool=False):
    db.query(LoanApplicationLog).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_loan_application_log_by_id(db: Session, id: int=0):
    return db.query(LoanApplicationLog).filter_by(id = id).first()

def get_loan_application_logs(db: Session, filters: Dict={}):
    query = db.query(LoanApplicationLog)
    if 'application_id' in filters:
        query = query.filter_by(application_id = filters['application_id'])
    if 'approved_user_id' in filters:
        query = query.filter_by(approved_user_id = filters['approved_user_id'])
    if 'rejected_user_id' in filters:
        query = query.filter_by(rejected_user_id = filters['rejected_user_id'])
    if 'is_top_up' in filters:
        query = query.filter_by(is_top_up = filters['is_top_up'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(LoanApplicationLog.created_at))
