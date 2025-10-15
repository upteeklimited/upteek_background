from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Bill(Base):

    __tablename__ = "bills"
     
    id = Column(BigInteger, primary_key=True, index=True)
    country_id = Column(BigInteger, default=0)
    currency_id = Column(BigInteger, default=0)
    category_id = Column(BigInteger, default=0)
    service_id = Column(BigInteger, default=0)
    provider_id = Column(BigInteger, default=0)
    operator_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    short_name = Column(String, nullable=True)
    label = Column(String, nullable=True)
    code = Column(String, nullable=True)
    amount = Column(Float, default=0)
    minimum_amount = Column(Float, default=0)
    maximum_amount = Column(Float, default=0)
    fee = Column(Float, default=0)
    commission = Column(Float, default=0)
    is_airtime = Column(SmallInteger, default=0)
    is_data = Column(SmallInteger, default=0)
    is_flat = Column(SmallInteger, default=0)
    has_bundles = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    meta_data = Column(Text, nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_bill(db: Session, country_id: int = 0, currency_id: int = 0, category_id: int = 0, service_id: int = 0, provider_id: int = 0, operator_id: int = 0, name: str = None, description: str = None, short_name: str = None, label: str = None, code: str = None, amount: float = 0, minimum_amount: float = 0, maximum_amount: float = 0, fee: float = 0, commission: float = 0, is_airtime: int = 0, is_data: int = 0, is_flat: int = 0, has_bundles: int = 0, status: int = 0, meta_data: str = None, commit: bool=False):
    bill = Bill(country_id=country_id, currency_id=currency_id, category_id=category_id, service_id=service_id, provider_id=provider_id, operator_id=operator_id, name=name, description=description, short_name=short_name, label=label, code=code, amount=amount, minimum_amount=minimum_amount, maximum_amount=maximum_amount, fee=fee, commission=commission, is_airtime=is_airtime, is_data=is_data, is_flat=is_flat, has_bundles=has_bundles, status=status, meta_data=meta_data, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(bill)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(bill)
    return bill

def update_bill(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Bill).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_bill(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Bill).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_bill(db: Session, id: int=0, commit: bool=False):
    db.query(Bill).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_bill_by_id(db: Session, id: int=0):
    return db.query(Bill).filter_by(id = id).first()

def get_bills(db: Session, filters: Dict={}):
    query = db.query(Bill)
    if 'country_id' in filters:
        query = query.filter_by(country_id = filters['country_id'])
    if 'category_id' in filters:
        query = query.filter_by(category_id = filters['category_id'])
    if 'service_id' in filters:
        query = query.filter_by(service_id = filters['service_id'])
    if 'provider_id' in filters:
        query = query.filter_by(provider_id = filters['provider_id'])
    if 'operator_id' in filters:
        query = query.filter_by(operator_id = filters['operator'])
    if 'code' in filters:
        query = query.filter_by(code = filters['code'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(Bill.created_at))

def count_bills(db: Session):
    return db.query(Bill).count()

def count_bills_by_code(db: Session, code: str=None):
    return db.query(Bill).filter_by(code = code).count()

def check_if_bill_exists(db: Session, code: str=None):
    count = count_bills_by_code(db=db, code=code)
    if count > 0:
        return True
    else:
        return False