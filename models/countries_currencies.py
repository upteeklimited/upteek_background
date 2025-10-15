from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class CountryCurrency(Base):

    __tablename__ = "countries_currencies"
     
    id = Column(BigInteger, primary_key=True, index=True)
    country_id = Column(BigInteger, default=0)
    currency_id = Column(BigInteger, default=0)
    is_main = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_country_currency(db: Session, country_id: int = 0, currency_id: int = 0, is_main: int = 0, status: int = 0, commit: bool=False):
    cc = CountryCurrency(country_id=country_id, currency_id=currency_id, is_main=is_main, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(cc)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(cc)
    return cc

def update_country_currency(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(CountryCurrency).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_country_currency(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(CountryCurrency).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_country_currency(db: Session, id: int=0, commit: bool=False):
    db.query(CountryCurrency).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_country_currency_by_id(db: Session, id: int=0):
    return db.query(CountryCurrency).filter_by(id = id).first()

def get_countries_currencies(db: Session):
    return db.query(CountryCurrency).filter(CountryCurrency.deleted_at == None).order_by(desc(CountryCurrency.id))

def get_countries_currencies_by_country_id(db: Session, country_id: int = 0):
    return db.query(CountryCurrency).filter_by(country_id = country_id).filter(CountryCurrency.deleted_at == None).order_by(desc(CountryCurrency.id))

def get_countries_currencies_by_currency_id(db: Session, currency_id: int = 0):
    return db.query(CountryCurrency).filter_by(currency_id = currency_id).filter(CountryCurrency.deleted_at == None).order_by(desc(CountryCurrency.id))