from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class GeneralLedgerAccountType(Base):

    __tablename__ = "general_ledger_account_types"
     
    id = Column(BigInteger, primary_key=True, index=True)
    country_id = Column(BigInteger, default=0)
    currency_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    account_code = Column(String, nullable=True)
    type_number = Column(Integer, default=0)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    authorized_by = Column(BigInteger, default=0)
    authorized_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    gls = relationship('GeneralLedgerAccount', back_populates='gl_type', foreign_keys='GeneralLedgerAccount.type_id')

def create_general_ledger_account_type(db: Session, country_id: int = 0, currency_id: int = 0, name: str = None, description: str = None, account_code: str = None, type_number: int = 0, status: int = 0, created_by: int = 0, authorized_by: int = 0, authorized_at: str = None, commit: bool=False):
    general_ledger_account_type = GeneralLedgerAccountType(country_id=country_id, currency_id=currency_id, name=name, description=description, account_code=account_code, type_number=type_number, status=status, created_by=created_by, authorized_by=authorized_by, authorized_at=authorized_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(general_ledger_account_type)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(general_ledger_account_type)
    return general_ledger_account_type

def update_general_ledger_account_type(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(GeneralLedgerAccountType).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_general_ledger_account_type(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(GeneralLedgerAccountType).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_general_ledger_account_type(db: Session, id: int=0, commit: bool=False):
    db.query(GeneralLedgerAccountType).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_last_general_ledger_account_type(db: Session):
    return db.query(GeneralLedgerAccountType).order_by(desc(GeneralLedgerAccountType.id)).first()

def get_single_general_ledger_account_type_by_id(db: Session, id: int=0):
    return db.query(GeneralLedgerAccountType).filter_by(id = id).first()

def get_single_general_ledger_account_type_by_account_code(db: Session, account_code: str=None):
    return db.query(GeneralLedgerAccountType).filter_by(account_code = account_code).first()

def get_general_ledger_account_types(db: Session, filters: Dict={}):
    query = db.query(GeneralLedgerAccountType)
    if 'country_id' in filters:
        query = query.filter_by(country_id = filters['country_id'])
    if 'currency_id' in filters:
        query = query.filter_by(currency_id = filters['currency_id'])
    if 'name' in filters:
        query = query.filter(GeneralLedgerAccountType.name.like('%' + filters['name'] + '%'))
    if 'account_code' in filters:
        query = query.filter(GeneralLedgerAccountType.account_code.like('%' + filters['account_code'] + '%'))
    if 'type_number' in filters:
        query = query.filter_by(type_number = filters['type_number'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(GeneralLedgerAccountType.created_at))

def get_ids_of_general_ledger_account_types(db: Session, filters: Dict={}):
    query = db.query(GeneralLedgerAccountType.id)
    if 'country_id' in filters:
        query = query.filter_by(country_id = filters['country_id'])
    if 'currency_id' in filters:
        query = query.filter_by(currency_id = filters['currency_id'])
    if 'name' in filters:
        query = query.filter(GeneralLedgerAccountType.name.like('%' + filters['name'] + '%'))
    if 'account_code' in filters:
        query = query.filter(GeneralLedgerAccountType.account_code.like('%' + filters['account_code'] + '%'))
    if 'type_number' in filters:
        query = query.filter_by(type_number = filters['type_number'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.scalars().all()