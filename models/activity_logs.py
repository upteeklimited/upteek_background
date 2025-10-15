from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Activity_Log(Base):

    __tablename__ = "activity_logs"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, default=0)
    gl_id = Column(BigInteger, default=0)
    account_id = Column(BigInteger, default=0)
    transaction_id = Column(BigInteger, default=0)
    application_id = Column(BigInteger, default=0)
    loan_id = Column(BigInteger, default=0)
    deposit_id = Column(BigInteger, default=0)
    order_id = Column(BigInteger, default=0)
    card_id = Column(BigInteger, default=0)
    activity_type = Column(Integer, default=0)
    activity_action = Column(String, nullable=True)
    activity_message = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_activity_log(db: Session, user_id: int = 0, gl_id: int = 0, account_id: int = 0, transaction_id: int = 0, application_id: int = 0, loan_id: int = 0, deposit_id: int = 0, order_id: int = 0, card_id: int = 0, activity_type: int = 0, activity_action: str = None, activity_message: str = None, status: int = 0, commit: bool=False):
    act_log = Activity_Log(user_id=user_id, gl_id=gl_id, account_id=account_id, transaction_id=transaction_id, application_id=application_id, loan_id=loan_id, deposit_id=deposit_id, order_id=order_id, card_id=card_id, activity_type=activity_type, activity_action=activity_action, activity_message=activity_message, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(act_log)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(act_log)
    return act_log

def update_activity_log(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Activity_Log).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_activity_log(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Activity_Log).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_activity_log(db: Session, id: int=0, commit: bool=False):
    db.query(Activity_Log).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_activity_log_by_id(db: Session, id: int=0):
    return db.query(Activity_Log).filter_by(id = id).first()

def get_activity_logs(db: Session, filters: Dict={}):
    query = db.query(Activity_Log)
    if 'gl_id' in filters:
        query = query.filter_by(gl_id = filters['gl_id'])
    if 'account_id' in filters:
        query = query.filter_by(account_id = filters['account_id'])
    if 'user_id' in filters:
        query = query.filter_by(user_id = filters['user_id'])
    if 'transaction_id' in filters:
        query = query.filter_by(transaction_id = filters['transaction_id'])
    if 'application_id' in filters:
        query = query.filter_by(application_id = filters['application_id'])
    if 'loan_id' in filters:
        query = query.filter_by(loan_id = filters['loan_id'])
    if 'deposit_id' in filters:
        query = query.filter_by(deposit_id = filters['deposit_id'])
    if 'order_id' in filters:
        query = query.filter_by(order_id = filters['order_id'])
    if 'card_id' in filters:
        query = query.filter_by(card_id = filters['card_id'])
    if 'activity_type' in filters:
        query = query.filter_by(activity_type = filters['activity_type'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(Activity_Log.created_at))