from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Trial_Balance_Header(Base):

    __tablename__ = "trial_balance_headers"
     
    id = Column(BigInteger, primary_key=True, index=True)
    header_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    value_date = Column(String, nullable=True)
    asset_positive_total = Column(Float, default=0)
    asset_negative_total = Column(Float, default=0)
    liability_positive_total = Column(Float, default=0)
    liability_negative_total = Column(Float, default=0)
    capital_positive_total = Column(Float, default=0)
    capital_negative_total = Column(Float, default=0)
    income_positive_total = Column(Float, default=0)
    income_negative_total = Column(Float, default=0)
    expense_positive_total = Column(Float, default=0)
    expense_negative_total = Column(Float, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_trial_balance_header(db: Session, header_id: int = 0, name: str = None, value_date: str = None, asset_positive_total: float = 0, asset_negative_total: float = 0, liability_positive_total: float = 0, liability_negative_total: float = 0, capital_positive_total: float = 0, capital_negative_total: float = 0, income_positive_total: float = 0, income_negative_total: float = 0, expense_positive_total: float = 0, expense_negative_total: float = 0, status: int = 0, commit: bool=False):
    tbh = Trial_Balance_Header(header_id=header_id, name=name, value_date=value_date, asset_positive_total=asset_positive_total, asset_negative_total=asset_negative_total, liability_positive_total=liability_positive_total, liability_negative_total=liability_negative_total, capital_positive_total=capital_positive_total, capital_negative_total=capital_negative_total, income_positive_total=income_positive_total, income_negative_total=income_negative_total, expense_positive_total=expense_positive_total, expense_negative_total=expense_negative_total, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(tbh)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(tbh)
    return tbh

def update_trial_balance_header(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Trial_Balance_Header).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_trial_balance_header(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Trial_Balance_Header).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_trial_balance_header(db: Session, id: int=0, commit: bool=False):
    db.query(Trial_Balance_Header).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_trial_balance_header_by_id(db: Session, id: int=0):
    return db.query(Trial_Balance_Header).filter_by(id = id).first()

def get_trial_balance_headers(db: Session, filters: Dict={}):
    query = db.query(Trial_Balance_Header)
    if 'header_id' in filters:
        query = query.filter_by(header_id = filters['header_id'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    if 'name' in filters:
        query = query.filter(Trial_Balance_Header.name.like("%" + filters['name'] + "%"))
    return query.order_by(desc(Trial_Balance_Header.created_at))