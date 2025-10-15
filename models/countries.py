from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Country(Base):

    __tablename__ = "countries"
     
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=True)
    language = Column(String, nullable=True)
    code = Column(String, nullable=True)
    code_two = Column(String, nullable=True)
    area_code = Column(String, nullable=True)
    base_timezone = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    flag = Column(Text, nullable=True)
    visibility = Column(SmallInteger, default=0)
    vat = Column(Float, default=0)
    wht = Column(Float, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    users = relationship("User", back_populates='country')


def create_country(db: Session, name: str = None, language: str = None, code: str = None, code_two: str = None, area_code: str = None, base_timezone: str = None, latitude: str = None,  longitude: str = None, flag: str = None, visibility: int = 0, vat: float = 0, wht: float = 0, status: int = 0, commit: bool=False):
    country = Country(name=name, language=language, code=code, code_two=code_two, area_code=area_code, base_timezone=base_timezone, latitude=latitude, longitude=longitude, flag=flag, visibility=visibility, vat=vat, wht=wht, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(country)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(country)
    return country

def update_country(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Country).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_country(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Country).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_country(db: Session, id: int=0, commit: bool=False):
    db.query(Country).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_country_by_id(db: Session, id: int=0):
    return db.query(Country).filter_by(id = id).first()

def get_single_country_by_code(db: Session, code: str=None):
    return db.query(Country).filter_by(code = code).first()

def get_countries(db: Session):
    return db.query(Country).filter(Country.deleted_at == None).order_by(desc(Country.id))
