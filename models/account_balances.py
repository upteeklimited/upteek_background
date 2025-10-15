from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Account_Balance(Base):

    __tablename__ = "account_balances"
     
    id = Column(BigInteger, primary_key=True, index=True)
    gl_id = Column(BigInteger, default=0)
    account_id = Column(BigInteger, default=0)
    balance = Column(Float, default=0)
    ledger_balance = Column(Float, default=0)
    gl_positive_balance = Column(Float, default=0)
    gl_negative_balance = Column(Float, default=0)
    account_status = Column(SmallInteger, default=0)
    is_eod = Column(SmallInteger, default=0)
    eod_date = Column(String, nullable=True)
    eod_prev_date = Column(String, nullable=True)
    is_eom = Column(SmallInteger, default=0)
    eom_date = Column(String, nullable=True)
    eom_prev_date = Column(String, nullable=True)
    eom_month_year = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_account_balance(db: Session, gl_id: int = 0, account_id: int = 0, balance: float = 0, ledger_balance: float = 0, gl_positive_balance: float = 0, gl_negative_balance: float = 0, account_status: int = 0, is_eod: int = 0, eod_date: str = None, eod_prev_date: str = None, is_eom: int = 0, eom_date: str = None, eom_prev_date: str = None, eom_month_year: str = None, status: int = 0, commit: bool=False):
    acct_bal = Account_Balance(gl_id=gl_id, account_id=account_id, balance=balance, ledger_balance=ledger_balance, gl_positive_balance=gl_positive_balance, gl_negative_balance=gl_negative_balance, account_status=account_status, is_eod=is_eod, eod_date=eod_date, eod_prev_date=eod_prev_date, is_eom=is_eom, eom_date=eom_date, eom_prev_date=eom_prev_date, eom_month_year=eom_month_year, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(acct_bal)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(acct_bal)
    return acct_bal

def update_account_balance(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Account_Balance).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_account_balance(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Account_Balance).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_account_balance(db: Session, id: int=0, commit: bool=False):
    db.query(Account_Balance).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_account_balance_by_id(db: Session, id: int=0):
    return db.query(Account_Balance).filter_by(id = id).first()

def get_account_balances(db: Session, filters: Dict={}):
    query = db.query(Account_Balance)
    if 'gl_id' in filters:
        query = query.filter_by(gl_id = filters['gl_id'])
    if 'account_id' in filters:
        query = query.filter_by(account_id = filters['account_id'])
    if 'is_eod' in filters:
        query = query.filter_by(is_eod = filters['is_eod'])
    if 'is_eom' in filters:
        query = query.filter_by(is_eom = filters['is_eom'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(Account_Balance.created_at))