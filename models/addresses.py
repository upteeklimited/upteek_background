from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Address(Base):

    __tablename__ = "addresses"
     
    id = Column(BigInteger, primary_key=True, index=True)
    country_id = Column(BigInteger, default=0)
    state_id = Column(BigInteger, default=0)
    city_id = Column(BigInteger, default=0)
    lga_id = Column(BigInteger, default=0)
    addressable_type = Column(String, nullable=True)
    addressable_id = Column(BigInteger, default=0)
    house_number = Column(String, nullable=True)
    street = Column(String, nullable=True)
    nearest_bus_stop = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    meta_data = Column(Text, nullable=True)
    is_primary = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    orders = relationship("Order", back_populates="address")


def create_address(db: Session, country_id: int = 0, state_id: int = 0, city_id: int = 0, lga_id: int = 0, addressable_type: str = None, addressable_id: int = 0, house_number: str = None, street: str = None, nearest_bus_stop: str = None, latitude: str = None,  longitude: str = None, meta_data: str = None, is_primary: int = 0, status: int = 0, commit: bool=False):
    address = Address(country_id=country_id, state_id=state_id, city_id=city_id, lga_id=lga_id, addressable_type=addressable_type, addressable_id=addressable_id, house_number=house_number, street=street, nearest_bus_stop=nearest_bus_stop, latitude=latitude, longitude=longitude, meta_data=meta_data, is_primary=is_primary, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(address)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(address)
    return address

def update_address(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Address).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_address(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Address).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_address(db: Session, id: int=0, commit: bool=False):
    db.query(Address).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_address_by_id(db: Session, id: int=0):
    return db.query(Address).filter_by(id = id).first()

def get_addresses(db: Session):
    return db.query(Address).filter(Address.deleted_at == None).order_by(desc(Address.id))

def get_addresses_by_addressable_type(db: Session, addressable_type: str=None):
    return db.query(Address).filter(and_(Address.deleted_at == None, Address.addressable_type == addressable_type)).order_by(desc(Address.id))

def get_addressable(db: Session, addressable_type: str=None, addressable_id: int=0, is_primary: int=0):
    return db.query(Address).filter(and_(Address.deleted_at == None, Address.addressable_type == addressable_type, Address.addressable_id == addressable_id, Address.is_primary == is_primary)).first()
