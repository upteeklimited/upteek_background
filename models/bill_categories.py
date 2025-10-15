from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class BillCategory(Base):

    __tablename__ = "bill_categories"
     
    id = Column(BigInteger, primary_key=True, index=True)
    country_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    code = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_bill_category(db: Session, country_id: int = 0, name: str = None, description: str = None, code: str = None, status: int = 0, commit: bool=False):
    bill_category = BillCategory(country_id=country_id, name=name, description=description, code=code, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(bill_category)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(bill_category)
    return bill_category

def update_bill_category(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(BillCategory).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_bill_category(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(BillCategory).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_bill_category(db: Session, id: int=0, commit: bool=False):
    db.query(BillCategory).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_bill_category_by_id(db: Session, id: int=0):
    return db.query(BillCategory).filter_by(id = id).first()

def get_single_bill_category_by_code(db: Session, code: str=None):
    return db.query(BillCategory).filter_by(code = code).first()

def get_bill_categories(db: Session, filters: Dict={}):
    query = db.query(BillCategory)
    if 'country_id' in filters:
        query = query.filter_by(country_id = filters['country_id'])
    if 'code' in filters:
        query = query.filter_by(code = filters['code'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(BillCategory.created_at))

def count_bill_categories(db: Session):
    return db.query(BillCategory).count()

def count_bill_categories_by_code(db: Session, code: str=None):
    return db.query(BillCategory).filter_by(code = code).count()

def check_bill_category_exist(db: Session, code: str = None):
    coun = count_bill_categories_by_code(db=db, code=code)
    if coun > 0:
        return True
    else:
        return False