from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class VirtualAccount(Base):

    __tablename__ = "virtual_accounts"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    account_id = Column(BigInteger, ForeignKey('accounts.id'))
    financial_institution_id = Column(BigInteger, ForeignKey('financial_institutions.id'))
    provider_id = Column(BigInteger, default=0)
    external_reference = Column(String, nullable=True)
    account_name = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    bank_name = Column(String, nullable=True)
    is_primary = Column(SmallInteger, default=0)
    is_generated = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    account = relationship('Account', back_populates='virtual_account', foreign_keys=[account_id])
    financial_institution = relationship('FinancialInstitution')

def create_virtual_account(db: Session, user_id: int = 0, account_id: int = 0, financial_institution_id: int = 0, provider_id: int = 0, external_reference: str = None, account_name: str = None, account_number: str = None, bank_name: str = None, status: int = 0, is_primary: int = 0, is_generated: int = 0, commit: bool=False):
    va = VirtualAccount(user_id=user_id, account_id=account_id, financial_institution_id=financial_institution_id, provider_id=provider_id, external_reference=external_reference, account_name=account_name, account_number=account_number, bank_name=bank_name, is_primary=is_primary, is_generated=is_generated, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(va)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(va)
    return va

def update_virtual_account(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(VirtualAccount).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_virtual_account(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(VirtualAccount).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_virtual_account(db: Session, id: int=0, commit: bool=False):
    db.query(VirtualAccount).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_virtual_account_by_id(db: Session, id: int=0):
    return db.query(VirtualAccount).filter_by(id = id).first()

def get_virtual_accounts(db: Session, filters: Dict={}):
    query = db.query(VirtualAccount)
    if 'user_id' in filters:
        query = query.filter_by(user_id = filters['user_id'])
    if 'account_id' in filters:
        query = query.filter_by(account_id = filters['account_id'])
    if 'financial_institution_id' in filters:
        query = query.filter_by(financial_institution_id = filters['financial_institution_id'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    if 'account_name' in filters:
        query = query.filter(VirtualAccount.account_name.like("%" + filters['account_name'] + "%"))
    if 'account_number' in filters:
        query = query.filter(VirtualAccount.account_number.like("%" + filters['account_number'] + "%"))
    return query.order_by(desc(VirtualAccount.created_at))