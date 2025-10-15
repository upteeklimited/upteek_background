from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Provider(Base):

    __tablename__ = "providers"
     
    id = Column(BigInteger, primary_key=True, index=True)
    gl_account_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    code = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_provider(db: Session, gl_account_id: int = 0, name: str = None, description: str = None, code: str = None, status: int = 0, commit: bool=False):
    provider = Provider(gl_account_id=gl_account_id, name=name, description=description, code=code, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(provider)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(provider)
    return provider

def update_provider(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Provider).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_provider(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Provider).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_provider(db: Session, id: int=0, commit: bool=False):
    db.query(Provider).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_provider_by_id(db: Session, id: int=0):
    return db.query(Provider).filter_by(id = id).first()

def get_single_provider_by_code(db: Session, code: str=None):
    return db.query(Provider).filter_by(code = code).first()

def get_providers(db: Session):
    return db.query(Provider).order_by(desc(Provider.created_at))

def check_provider_exist(db: Session, code: str=None):
    return db.query(Provider).filter_by(code = code).count()