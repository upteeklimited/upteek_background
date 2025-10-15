from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Medium_Pivot(Base):

    __tablename__ = "media_pivots"
     
    id = Column(BigInteger, primary_key=True, index=True)
    medium_id = Column(BigInteger, default=0)
    mediumable_type = Column(String, nullable=True)
    mediumable_id = Column(BigInteger, default=0)
    meta_data = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_medium_pivot(db: Session, medium_id: int = 0, mediumable_type: str = None, mediumable_id: int = 0, meta_data: str = None, status: int = 0, commit: bool=False):
    medium_pivot = Medium_Pivot(medium_id=medium_id, mediumable_type=mediumable_type, mediumable_id=mediumable_id, meta_data=meta_data, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(medium_pivot)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(medium_pivot)
    return medium_pivot

def update_medium_pivot(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Medium_Pivot).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_medium_pivot(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Medium_Pivot).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_medium_pivot(db: Session, id: int=0, commit: bool=False):
    db.query(Medium_Pivot).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_medium_pivot(db: Session, id: int=0):
    return db.query(Medium_Pivot).filter_by(id = id).first()

def get_medium_pivot_by_medium_id(db: Session, medium_id: int=0):
    return db.query(Medium_Pivot).filter_by(medium_id = medium_id).first()

def get_medium_pivot_by_mediumable_type_and_mediumable_id(db: Session, mediumable_type: str=None, mediumable_id: int=0):
    return db.query(Medium_Pivot).filter_by(mediumable_type = mediumable_type, mediumable_id = mediumable_id).first()

def get_medium_pivot_by_mediumable_type_and_mediumable_id_and_status(db: Session, mediumable_type: str=None, mediumable_id: int=0, status: int=0):
    return db.query(Medium_Pivot).filter_by(mediumable_type = mediumable_type, mediumable_id = mediumable_id, status = status).first()

def get_media_pivots(db: Session, filter: dict={}):
    query = db.query(Medium_Pivot).filter(Medium_Pivot.deleted_at == None).order_by(desc(Medium_Pivot.id))
    if filter.get('medium_id') != None:
        query = query.filter(Medium_Pivot.medium_id == filter['medium_id'])
    if filter.get('mediumable_type') != None:
        query = query.filter(Medium_Pivot.mediumable_type == filter['mediumable_type'])
    if filter.get('mediumable_id') != None:
        query = query.filter(Medium_Pivot.mediumable_id == filter['mediumable_id'])
    if filter.get('status') != None:
        query = query.filter(Medium_Pivot.status == filter['status'])
    return query.order_by(desc(Medium_Pivot.id))