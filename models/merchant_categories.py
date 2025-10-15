from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class MerchantCategory(Base):

    __tablename__ = "merchant_categories"
     
    id = Column(BigInteger, primary_key=True, index=True)
    industry_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_merchant_category(db: Session, industry_id: int = 0, name: str = None, description: str = None, status: int = 0, commit: bool=False):
    merchant_category = MerchantCategory(industry_id=industry_id, name=name, description=description, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(merchant_category)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(merchant_category)
    return merchant_category

def update_merchant_category(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(MerchantCategory).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_merchant_category(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(MerchantCategory).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_merchant_category(db: Session, id: int=0, commit: bool=False):
    db.query(MerchantCategory).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_merchant_category_by_id(db: Session, id: int=0):
    return db.query(MerchantCategory).filter_by(id = id).first()

def get_merchant_categories(db: Session):
    return db.query(MerchantCategory).filter(MerchantCategory.deleted_at == None).order_by(desc(MerchantCategory.id))

def get_merchant_categories_by_industry_id(db: Session, industry_id: int=0):
    return db.query(MerchantCategory).filter_by(industry_id = industry_id).filter(MerchantCategory.deleted_at == None).order_by(desc(MerchantCategory.id))