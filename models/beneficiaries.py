from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Beneficiary(Base):

    __tablename__ = "beneficiaries"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, default=0)
    institution_id = Column(BigInteger, default=0)
    provider_id = Column(BigInteger, default=0)
    external_reference = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    account_name = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_beneficiary(db: Session, user_id: int = 0, institution_id: int = 0, provider_id: int = 0, external_reference: str = None, account_number: str = None, account_name: str = None, status: int = 0, commit: bool=False):
    beneficiary = Beneficiary(user_id=user_id, institution_id=institution_id, provider_id=provider_id, external_reference=external_reference, account_number=account_number, account_name=account_name, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(beneficiary)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(beneficiary)
    return beneficiary

def update_beneficiary(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Beneficiary).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_beneficiary(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Beneficiary).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_beneficiary(db: Session, id: int=0, commit: bool=False):
    db.query(Beneficiary).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_beneficiary_by_id(db: Session, id: int=0):
    return db.query(Beneficiary).filter_by(id = id).first()

def get_beneficiaries(db: Session, filters: Dict={}):
    query = db.query(Beneficiary)
    if 'user_id' in filters:
        query = query.filter(Beneficiary.user_id == filters['user_id'])
    if 'institution_id' in filters:
        query = query.filter(Beneficiary.institution_id == filters['institution_id'])
    if 'account_number' in filters:
        query = query.filter(Beneficiary.account_number.like("%"+filters['account_number']+"%"))
    if 'account_name' in filters:
        query = query.filter(Beneficiary.account_name.like("%"+filters['account_name']+"%"))
    if 'status' in filters:
        query = query.filter(Beneficiary.status == filters['status'])
    return query.order_by(desc(Beneficiary.created_at))
