from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Trial_Balance(Base):

    __tablename__ = "trial_balances"
     
    id = Column(BigInteger, primary_key=True, index=True)
    category_id = Column(BigInteger, default=0)
    parent_id = Column(BigInteger, default=0)
    gl_id = Column(BigInteger, default=0)
    balance = Column(Float, default=0)
    positive_balance = Column(Float, default=0)
    negative_balance = Column(Float, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_trial_balance(db: Session, category_id: int = 0, parent_id: int = 0, gl_id: int = 0, balance: float = 0, positive_balance: float = 0, negative_balance: float = 0, status: int = 0, commit: bool=False):
    tb = Trial_Balance(category_id=category_id, parent_id=parent_id, gl_id=gl_id, balance=balance, positive_balance=positive_balance, negative_balance=negative_balance, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(tb)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(tb)
    return tb

def update_trial_balance(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Trial_Balance).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_trial_balance(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Trial_Balance).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_trial_balance(db: Session, id: int=0, commit: bool=False):
    db.query(Trial_Balance).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_trial_balance_by_id(db: Session, id: int=0):
    return db.query(Trial_Balance).filter_by(id = id).first()

def get_trial_balances(db: Session, filters: Dict={}):
    query = db.query(Trial_Balance)
    if 'parent_id' in filters:
        query = query.filter_by(parent_id = filters['parent_id'])
    if 'category_id' in filters:
        query = query.filter_by(category_id = filters['category_id'])
    if 'gl_id' in filters:
        query = query.filter_by(gl_id = filters['gl_id'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(Trial_Balance.created_at))