from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class UserDevice(Base):

    __tablename__ = "user_devices"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    app_version = Column(String, nullable=True)
    build_number = Column(String, nullable=True)
    device_brand = Column(String, nullable=True)
    device_id = Column(String, nullable=True)
    platform = Column(String, nullable=True)
    platform_version = Column(String, nullable=True)
    operating_system = Column(String, nullable=True)
    browser = Column(String, nullable=True)
    fbt = Column(String, nullable=True)
    last_ip_address = Column(String, nullable=True)
    last_latitude = Column(String, nullable=True)
    last_longitude = Column(String, nullable=True)
    fingerprint = Column(String, nullable=True)
    is_mobile = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_user_device(db: Session, user_id: int = 0, name: str = None, app_version: str = None, build_number: str = None, device_brand: str = None, device_id: str = None, platform: str = None, platform_version: str = None, operating_system: str = None, browser: str = None, fbt: str = None, last_ip_address: str = None, last_latitude: str = None, last_longitude: str = None, fingerprint: str = None, is_mobile: int = 0, status: int = 0, commit: bool=False):
    user_device = UserDevice(user_id=user_id, name=name, app_version=app_version, build_number=build_number, device_brand=device_brand, device_id=device_id, platform=platform, platform_version=platform_version, operating_system=operating_system, browser=browser, fbt=fbt, last_ip_address=last_ip_address, last_latitude=last_latitude, last_longitude=last_longitude, fingerprint=fingerprint, is_mobile=is_mobile, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(user_device)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(user_device)
    return user_device

def update_user_device(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(UserDevice).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_user_device(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(UserDevice).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_user_device(db: Session, id: int=0, commit: bool=False):
    db.query(UserDevice).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_user_device_by_id(db: Session, id: int=0):
    return db.query(UserDevice).filter_by(id = id).first()

def get_user_devices(db: Session):
    return db.query(UserDevice).filter(UserDevice.deleted_at == None).order_by(desc(UserDevice.id))

def get_user_devices_by_user_id(db: Session, user_id: int = 0):
    return db.query(UserDevice).filter_by(user_id = user_id).filter(UserDevice.deleted_at == None).order_by(desc(UserDevice.id))

