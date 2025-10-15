from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Entity(Base):

    __tablename__ = "entities"
     
    id = Column(BigInteger, primary_key=True, index=True)
    entitiable_type = Column(String, nullable=True)
    entitiable_id = Column(BigInteger, default=0)
    entity_type = Column(String, nullable=True)
    name = Column(String, nullable=True)
    legal_name = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    tax_id = Column(String, nullable=True)
    registration_type = Column(String, nullable=True)
    registration_number = Column(String, nullable=True)
    registration_date = Column(String, nullable=True)
    search_number = Column(String, nullable=True)
    shared_capital = Column(String, nullable=True)
    address = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    registration_status = Column(String, nullable=True)
    meta_data = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_entity(db: Session, entitiable_type: str = None, entitiable_id: int = 0, entity_type: str = None, name: str = None, legal_name: str = None, industry: str = None,  email: str = None, phone_number: str = None, tax_id: str = None, registration_type: str = None, registration_number: str = None, registration_date: str = None, search_number: str = None, shared_capital: str = None, address: str = None, state: str = None, country: str = None, registration_status: str = None, meta_data: str = None, status: int = 0, commit: bool=False):
    entity = Entity(entitiable_type=entitiable_type, entitiable_id=entitiable_id, entity_type=entity_type, name=name, legal_name=legal_name, industry=industry, email=email, phone_number=phone_number, tax_id=tax_id, registration_type=registration_type, registration_number=registration_number, registration_date=registration_date, search_number=search_number, shared_capital=shared_capital, address=address, state=state, country=country, registration_status=registration_status, meta_data=meta_data, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(entity)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(entity)
    return entity

def update_entity(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Entity).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_entity(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Entity).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_entity(db: Session, id: int=0, commit: bool=False):
    db.query(Entity).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_entity_by_id(db: Session, id: int=0):
    return db.query(Entity).filter_by(id = id).first()

def get_entities(db: Session):
    return db.query(Entity).filter(Entity.deleted_at == None).order_by(desc(Entity.id))

def get_people_by_entitiable_type(db: Session, entitiable_type: str=None):
    return db.query(Entity).filter(and_(Entity.deleted_at == None, Entity.entitiable_type == entitiable_type)).order_by(desc(Entity.id))

def get_entitable(db: Session, entitiable_type: str=None, entitiable_id: int=0):
    return db.query(Entity).filter(and_(Entity.deleted_at == None, Entity.entitiable_type == entitiable_type, Entity.entitiable_id == entitiable_id)).first()
