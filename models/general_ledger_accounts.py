from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class GeneralLedgerAccount(Base):

    __tablename__ = "general_ledger_accounts"
     
    id = Column(BigInteger, primary_key=True, index=True)
    type_id = Column(BigInteger, ForeignKey('general_ledger_account_types.id'))
    parent_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    balance = Column(Float, default=0)
    status = Column(SmallInteger, default=0)
    manager_id = Column(BigInteger, default=0)
    created_by = Column(BigInteger, default=0)
    authorized_by = Column(BigInteger, default=0)
    authorized_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    gl_type = relationship('GeneralLedgerAccountType', back_populates='gls', foreign_keys=[type_id])
    transactions = relationship('Transaction', back_populates='general_ledger', foreign_keys='Transaction.gl_id')

def create_general_ledger_account(db: Session, type_id: int = 0, parent_id: int = 0, name: str = None, account_number: str = None, description: str = None, balance: float = 0, status: int = 0, manager_id: int = 0, created_by: int = 0, authorized_by: int = 0, authorized_at: str = None, commit: bool=False):
    general_ledger_account = GeneralLedgerAccount(type_id=type_id, parent_id=parent_id, name=name, account_number=account_number, description=description, balance=balance, status=status, manager_id=manager_id, created_by=created_by, authorized_by=authorized_by, authorized_at=authorized_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(general_ledger_account)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(general_ledger_account)
    return general_ledger_account

def update_general_ledger_account(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(GeneralLedgerAccount).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_general_ledger_account(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(GeneralLedgerAccount).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_general_ledger_account(db: Session, id: int=0, commit: bool=False):
    db.query(GeneralLedgerAccount).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_general_ledger_account_by_id(db: Session, id: int=0):
    return db.query(GeneralLedgerAccount).filter_by(id = id).first()

def get_single_general_ledger_account_by_account_number(db: Session, account_number: str = None):
    return db.query(GeneralLedgerAccount).filter_by(account_number = account_number).first()

def get_last_general_ledger_account(db: Session):
    return db.query(GeneralLedgerAccount).order_by(desc(GeneralLedgerAccount.id)).first()

def get_general_ledger_accounts(db: Session, filters: Dict={}):
    query = db.query(GeneralLedgerAccount)
    if 'type_id' in filters:
        query = query.filter_by(type_id = filters['type_id'])
    if 'type_ids' in filters:
        query = query.filter(GeneralLedgerAccount.id.in_(filters['type_ids']))
    if 'parent_id' in filters:
        query = query.filter_by(parent_id = filters['parent_id'])
    if 'manager_id' in filters:
        query = query.filter_by(manager_id = filters['manager_id'])
    if 'name' in filters:
        query = query.filter(GeneralLedgerAccount.name.like('%'+filters['name']+'%'))
    if 'account_number' in filters:
        query = query.filter(GeneralLedgerAccount.account_number.like('%'+filters['account_number']+'%'))
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(GeneralLedgerAccount.created_at))

def filter_general_ledger_accounts(db: Session, filters: Dict={}):
    query = db.query(GeneralLedgerAccount)
    if 'type_id' in filters:
        query = query.filter_by(type_id = filters['type_id'])
    if 'type_ids' in filters:
        query = query.filter(GeneralLedgerAccount.id.in_(filters['type_ids']))
    if 'parent_id' in filters:
        query = query.filter_by(parent_id = filters['parent_id'])
    if 'manager_id' in filters:
        query = query.filter_by(manager_id = filters['manager_id'])
    if 'name' in filters:
        query = query.filter(GeneralLedgerAccount.name.like('%'+filters['name']+'%'))
    if 'account_number' in filters:
        query = query.filter(GeneralLedgerAccount.account_number.like('%'+filters['account_number']+'%'))
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(GeneralLedgerAccount.created_at)).all()

def search_general_ledger_accounts(db: Session, search: str = None):
    query = db.query(GeneralLedgerAccount)
    if search is not None:
        query = query.filter(or_(GeneralLedgerAccount.name.like('%'+search+'%'), GeneralLedgerAccount.account_number.like('%'+search+'%')))
    return query.order_by(desc(GeneralLedgerAccount.created_at)).all()

def get_ids_of_general_ledger_accounts(db: Session, filters: Dict={}):
    query = db.query(GeneralLedgerAccount)
    if 'type_id' in filters:
        query = query.filter_by(type_id = filters['type_id'])
    if 'type_ids' in filters:
        query = query.filter(GeneralLedgerAccount.id.in_(filters['type_ids']))
    if 'parent_id' in filters:
        query = query.filter_by(parent_id = filters['parent_id'])
    if 'manager_id' in filters:
        query = query.filter_by(manager_id = filters['manager_id'])
    if 'name' in filters:
        query = query.filter(GeneralLedgerAccount.name.like('%'+filters['name']+'%'))
    if 'account_number' in filters:
        query = query.filter(GeneralLedgerAccount.account_number.like('%'+filters['account_number']+'%'))
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.scalars().all()
