from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class State(Base):

    __tablename__ = "states"
     
    id = Column(BigInteger, primary_key=True, index=True)
    country_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    capital = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_state(db: Session, country_id: int = 0, name: str = None, capital: str = None, latitude: str = None,  longitude: str = None, status: int = 0, commit: bool=False):
    state = State(country_id=country_id, name=name, capital=capital, latitude=latitude, longitude=longitude, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(state)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(state)
    return state

def update_state(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(State).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_state(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(State).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_state(db: Session, id: int=0, commit: bool=False):
    db.query(State).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_state_by_id(db: Session, id: int=0):
    return db.query(State).filter_by(id = id).first()

def get_states(db: Session):
    return db.query(State).filter(State.deleted_at == None).order_by(desc(State.id))

def get_states_by_country_id(db: Session, country_id: int=0):
    return db.query(State).filter(and_(State.deleted_at == None, State.country_id == country_id)).order_by(desc(State.id))
