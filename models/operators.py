from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Operator(Base):

    __tablename__ = "operators"
     
    id = Column(BigInteger, primary_key=True, index=True)
    country_id = Column(BigInteger, default=0)
    category_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    code = Column(String, nullable=True)
    logo = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_operator(db: Session, country_id: int = 0, category_id: int = 0, name: str = None, description: str = None, code: str = None, logo: str = None, status: int = 0, commit: bool=False):
    operator = Operator(country_id=country_id, category_id=category_id, name=name, description=description, code=code, logo=logo, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(operator)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(operator)
    return operator

def update_operator(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Operator).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_operator(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Operator).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_operator(db: Session, id: int=0, commit: bool=False):
    db.query(Operator).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_operator_by_id(db: Session, id: int=0):
    return db.query(Operator).filter_by(id = id).first()

def get_operators(db: Session, filters: Dict={}):
    query = db.query(Operator)
    if 'country_id' in filters:
        query = query.filter_by(country_id = filters['country_id'])
    if 'category_id' in filters:
        query = query.filter_by(category_id = filters['category_id'])
    if 'code' in filters:
        query = query.filter_by(code = filters['code'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(Operator.created_at))
