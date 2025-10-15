from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Medium(Base):

    __tablename__ = "media"
     
    id = Column(BigInteger, primary_key=True, index=True)
    merchant_id = Column(BigInteger, default=0)
    mediumable_type = Column(String, nullable=True)
    mediumable_id = Column(BigInteger, default=0)
    file_type = Column(String, nullable=True)
    file_name = Column(String, nullable=True)
    file_description = Column(Text, nullable=True)
    file_path = Column(Text, nullable=True)
    file_url = Column(Text, nullable=True)
    meta_data = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_medium(db: Session, merchant_id: int = 0, mediumable_type: str = None, mediumable_id: int = 0, file_type: str = None, file_name: str = None, file_description: str = None, file_path: str = None,  file_url: str = None, meta_data: str = None, status: int = 0, created_by: int = 0, commit: bool=False):
    medium = Medium(merchant_id=merchant_id, mediumable_type=mediumable_type, mediumable_id=mediumable_id, file_type=file_type, file_name=file_name, file_description=file_description, file_path=file_path, file_url=file_url, meta_data=meta_data, status=status, created_by=created_by, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(medium)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(medium)
    return medium

def update_medium(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Medium).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_medium(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Medium).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_medium(db: Session, id: int=0, commit: bool=False):
    db.query(Medium).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_medium_by_id(db: Session, id: int=0):
    return db.query(Medium).filter_by(id = id).first()

def get_media(db: Session):
    return db.query(Medium).filter(Medium.deleted_at == None).order_by(desc(Medium.id))

def get_media_by_mediumable_type(db: Session, mediumable_type: str=None):
    return db.query(Medium).filter(and_(Medium.deleted_at == None, Medium.mediumable_type == mediumable_type)).order_by(desc(Medium.id))

def get_mediumable(db: Session, mediumable_type: str=None, mediumable_id: int=0):
    return db.query(Medium).filter(and_(Medium.deleted_at == None, Medium.mediumable_type == mediumable_type, Medium.mediumable_id == mediumable_id)).first()
