from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Person(Base):

    __tablename__ = "people"
     
    id = Column(BigInteger, primary_key=True, index=True)
    personable_type = Column(String, nullable=True)
    personable_id = Column(BigInteger, default=0)
    person_type = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    other_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    mothers_maiden_name = Column(String, nullable=True)
    date_of_birth = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    marital_status = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    avatar = Column(Text, nullable=True)
    nationality = Column(String, nullable=True)
    occupation = Column(String, nullable=True)
    shareholding = Column(String, nullable=True)
    id_document_file = Column(Text, nullable=True)
    id_document_type = Column(String, nullable=True)
    id_document_value = Column(String, nullable=True)
    id_issuance_date = Column(String, nullable=True)
    id_expiration_date = Column(String, nullable=True)
    politically_exposed = Column(SmallInteger, default=0)
    meta_data = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_person(db: Session, personable_type: str = None, personable_id: int = 0, person_type: str = None, first_name: str = None, other_name: str = None, last_name: str = None,  mothers_maiden_name: str = None, date_of_birth: str = None, gender: str = None, marital_status: str = None, bio: str = None, avatar: str = None, nationality: str = None, occupation: str = None, id_document_file: str = None, id_document_type: str = None, id_document_value: str = None, id_issuance_date: str = None, id_expiration_date: str = None, politically_exposed: int = 0, meta_data: str = None, status: int = 0, commit: bool=False):
    person = Person(personable_type=personable_type, personable_id=personable_id, person_type=person_type, first_name=first_name, other_name=other_name, last_name=last_name, mothers_maiden_name=mothers_maiden_name, date_of_birth=date_of_birth, gender=gender, marital_status=marital_status, bio=bio, avatar=avatar, nationality=nationality, occupation=occupation, id_document_file=id_document_file, id_document_type=id_document_type, id_document_value=id_document_value, id_issuance_date=id_issuance_date, id_expiration_date=id_expiration_date, politically_exposed=politically_exposed, meta_data=meta_data, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(person)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(person)
    return person

def update_person(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Person).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_person(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Person).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_person(db: Session, id: int=0, commit: bool=False):
    db.query(Person).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_person_by_id(db: Session, id: int=0):
    return db.query(Person).filter_by(id = id).first()

def get_people(db: Session):
    return db.query(Person).filter(Person.deleted_at == None).order_by(desc(Person.id))

def get_people_by_personable_type(db: Session, personable_type: str=None):
    return db.query(Person).filter(and_(Person.deleted_at == None, Person.personable_type == personable_type)).order_by(desc(Person.id))

def get_personable(db: Session, personable_type: str=None, personable_id: int=0):
    return db.query(Person).filter(and_(Person.deleted_at == None, Person.personable_type == personable_type, Person.personable_id == personable_id)).first()
