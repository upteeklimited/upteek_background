from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Trial_Balance_Category(Base):

    __tablename__ = "trial_balance_categories"
     
    id = Column(BigInteger, primary_key=True, index=True)
    header_id = Column(BigInteger, default=0)
    category_id = Column(BigInteger, default=0)
    type_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    type_action = Column(Integer, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_trial_balance_category(db: Session, header_id: int = 0, category_id: int = 0, type_id: int = 0, name: str = None, type_action: int = 0, status: int = 0, commit: bool=False):
    tbc = Trial_Balance_Category(header_id=header_id, category_id=category_id, type_id=type_id, name=name, type_action=type_action, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(tbc)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(tbc)
    return tbc

def update_trial_balance_category(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Trial_Balance_Category).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_trial_balance_category(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Trial_Balance_Category).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_trial_balance_category(db: Session, id: int=0, commit: bool=False):
    db.query(Trial_Balance_Category).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_trial_balance_category_by_id(db: Session, id: int=0):
    return db.query(Trial_Balance_Category).filter_by(id = id).first()

def get_trial_balance_categories(db: Session, filters: Dict={}):
    query = db.query(Trial_Balance_Category)
    if 'header_id' in filters:
        query = query.filter_by(header_id = filters['header_id'])
    if 'category_id' in filters:
        query = query.filter_by(category_id = filters['category_id'])
    if 'type_id' in filters:
        query = query.filter_by(type_id = filters['type_id'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    if 'name' in filters:
        query = query.filter(Trial_Balance_Category.name.like("%" + filters['name'] + "%"))
    return query.order_by(desc(Trial_Balance_Category.created_at))