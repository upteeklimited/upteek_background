from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class LGA(Base):

    __tablename__ = "l_g_a_s"
     
    id = Column(BigInteger, primary_key=True, index=True)
    state_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_lga(db: Session, state_id: int = 0, name: str = None, latitude: str = None,  longitude: str = None, status: int = 0, commit: bool=False):
    lga = LGA(state_id=state_id, name=name, latitude=latitude, longitude=longitude, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(lga)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(lga)
    return lga

def update_lga(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(LGA).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_lga(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(LGA).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_lga(db: Session, id: int=0, commit: bool=False):
    db.query(LGA).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_lga_by_id(db: Session, id: int=0):
    return db.query(LGA).filter_by(id = id).first()

def get_lgas(db: Session):
    return db.query(LGA).filter(LGA.deleted_at == None).order_by(desc(LGA.id))

def get_lgas_by_state_id(db: Session, state_id: int=0):
    return db.query(LGA).filter(and_(LGA.deleted_at == None, LGA.state_id == state_id)).order_by(desc(LGA.id))
