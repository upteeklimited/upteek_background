from typing import Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from database.custom_types import JSONText
from sqlalchemy.orm import relationship


class Merchant_User(Base):

    __tablename__ = "merchants_users"
     
    id = Column(BigInteger, primary_key=True, index=True)
    merchant_id = Column(BigInteger, ForeignKey('merchants.id'))
    user_id = Column(BigInteger, ForeignKey('users.id'))
    role = Column(Integer, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    user = relationship('User')
    merchant = relationship('Merchant')

def create_merchant_user(db: Session, merchant_id: int = 0, user_id: int = 0, role: int = 0, status: int = 0, commit: bool=False):
    merchant_user = Merchant_User(merchant_id=merchant_id, user_id=user_id, role=role, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(merchant_user)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(merchant_user)
    return merchant_user

def update_merchant_user(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Merchant_User).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_merchant_user(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Merchant_User).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_merchant_user(db: Session, id: int=0, commit: bool=False):
    db.query(Merchant_User).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_merchant_user_by_id(db: Session, id: int=0):
    return db.query(Merchant_User).filter_by(id = id).first()

def get_merchants_users(db: Session, filters: Dict={}):
    query = db.query(Merchant_User)
    if 'merchant_id' in filters:
        query = query.filter_by(merchant_id = filters['merchant_id'])
    if 'user_id' in filters:
        query = query.filter_by(user_id = filters['user_id'])
    if 'role' in filters:
        query = query.filter_by(role = filters['role'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(Merchant_User.created_at))

