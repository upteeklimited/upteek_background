from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class SystemConfiguration(Base):

    __tablename__ = "system_configurations"
     
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=True)
    single_value = Column(String, nullable=True)
    multi_value = Column(Text, nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_system_configuration(db: Session, name: str = None, single_value: str = None, multi_value: str = None, commit: bool=False):
    system_configuration = SystemConfiguration(name=name, single_value=single_value, multi_value=multi_value, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(system_configuration)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(system_configuration)
    return system_configuration

def update_system_configuration(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(SystemConfiguration).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_system_configuration(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(SystemConfiguration).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_system_configuration(db: Session, id: int=0, commit: bool=False):
    db.query(SystemConfiguration).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_system_configuration_by_id(db: Session, id: int=0):
    return db.query(SystemConfiguration).filter_by(id = id).first()

def get_single_system_configuration_by_name(db: Session, name: str = None):
    return db.query(SystemConfiguration).filter_by(name = name).first()

def get_system_configurations(db: Session):
    return db.query(SystemConfiguration).filter(SystemConfiguration.deleted_at == None).order_by(desc(SystemConfiguration.id))