from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class MerchantIndustry(Base):

    __tablename__ = "merchant_industries"
     
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_merchant_industry(db: Session, name: str = None, description: str = None, status: int = 0, commit: bool=False):
    merchant_industry = MerchantIndustry(name=name, description=description, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(merchant_industry)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(merchant_industry)
    return merchant_industry

def update_merchant_industry(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(MerchantIndustry).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_merchant_industry(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(MerchantIndustry).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_merchant_industry(db: Session, id: int=0, commit: bool=False):
    db.query(MerchantIndustry).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_merchant_industry_by_id(db: Session, id: int=0):
    return db.query(MerchantIndustry).filter_by(id = id).first()

def get_merchant_industries(db: Session):
    return db.query(MerchantIndustry).filter(MerchantIndustry.deleted_at == None).order_by(desc(MerchantIndustry.id))
