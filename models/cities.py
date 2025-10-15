from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class City(Base):

    __tablename__ = "cities"
     
    id = Column(BigInteger, primary_key=True, index=True)
    state_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    is_capital = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_city(db: Session, state_id: int = 0, name: str = None, latitude: str = None,  longitude: str = None, is_capital: int = 0, status: int = 0, commit: bool=False):
    city = City(state_id=state_id, name=name, latitude=latitude, longitude=longitude, is_capital=is_capital, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(city)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(city)
    return city

def update_city(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(City).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_city(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(City).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_city(db: Session, id: int=0, commit: bool=False):
    db.query(City).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_city_by_id(db: Session, id: int=0):
    return db.query(City).filter_by(id = id).first()

def get_capital_city(db: Session, state_id: int=0):
    return db.query(City).filter(and_(City.deleted_at == None, City.state_id == state_id, City.is_capital == 1)).first()

def get_cities(db: Session):
    return db.query(City).filter(City.deleted_at == None).order_by(desc(City.id))

def get_cities_by_state_id(db: Session, state_id: int=0):
    return db.query(City).filter(and_(City.deleted_at == None, City.state_id == state_id)).order_by(desc(City.id))
