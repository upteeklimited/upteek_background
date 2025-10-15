from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class UserDeviceLog(Base):

    __tablename__ = "user_device_logs"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_device_id = Column(BigInteger, default=0)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    resource_path = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_user_device_log(db: Session, user_device_id: int = 0, latitude: str = None, longitude: str = None, resource_path: str = None, ip_address: str = None, status: int = 0, commit: bool=False):
    user_device_log = UserDeviceLog(user_device_id=user_device_id, latitude=latitude, longitude=longitude, resource_path=resource_path, ip_address=ip_address, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(user_device_log)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(user_device_log)
    return user_device_log

def update_user_device_log(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(UserDeviceLog).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_user_device_log(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(UserDeviceLog).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_user_device_log(db: Session, id: int=0, commit: bool=False):
    db.query(UserDeviceLog).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_user_device_log_by_id(db: Session, id: int=0):
    return db.query(UserDeviceLog).filter_by(id = id).first()

def get_user_devices_logs(db: Session):
    return db.query(UserDeviceLog).filter(UserDeviceLog.deleted_at == None).order_by(desc(UserDeviceLog.id))

def get_user_device_logs_by_user_device_id(db: Session, user_device_id: int = 0):
    return db.query(UserDeviceLog).filter_by(user_device_id = user_device_id).filter(UserDeviceLog.deleted_at == None).order_by(desc(UserDeviceLog.id))

