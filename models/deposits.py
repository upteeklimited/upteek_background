from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Deposit(Base):

    __tablename__ = "deposits"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    merchant_id = Column(BigInteger, ForeignKey("merchants.id"))
    gl_id = Column(BigInteger, ForeignKey("general_ledger_accounts.id"))
    account_id = Column(BigInteger, ForeignKey("accounts.id"))
    amount = Column(Float, default=0)
    rate = Column(Float, default=0)
    tenure = Column(Integer, default=0)
    yield_amount = Column(Float, default=0)
    current_value = Column(Float, default=0)
    withholding_tax = Column(Float, default=0)
    vat = Column(Float, default=0)
    receiving_account_principal_id = Column(BigInteger, default=0)
    receiving_account_interest_id = Column(BigInteger, default=0)
    rollover_principal = Column(Float, default=0)
    rollover_interest = Column(Float, default=0)
    rollover_at_maturity = Column(SmallInteger, default=0)
    liquidation_charge = Column(Float, default=0)
    rollover_count = Column(Integer, default=0)
    paid_interest_status = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    meta_data = Column(Text, nullable=True)
    created_by = Column(BigInteger, default=0)
    authorized_by = Column(BigInteger, default=0)
    matured_at = Column(TIMESTAMP(timezone=True), nullable=True)
    liquidated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    authorized_at = Column(TIMESTAMP(timezone=True), nullable=True)
    rollover_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    account = relationship('Account', back_populates='deposit')

def create_deposit(db: Session, user_id: int = 0, merchant_id: int = 0, gl_id: int = 0, account_id: int = 0, amount: float = 0, rate: float = 0, tenure: int = 0, yield_amount: float = 0, current_value: float = 0, withholding_tax: float = 0, vat: float = 0, receiving_account_principal_id: int = 0, receiving_account_interest_id: int = 0, rollover_principal: float = 0, rollover_interest: float = 0, rollover_at_maturity: int = 0, liquidation_charge: float = 0, rollover_count: int = 0, paid_interest_status: int = 0, status: int = 0, meta_data: str = None, created_by: int = 0, authorized_by: int = 0, matured_at: str = None, liquidated_at: str = None, authorized_at: str = None, rollover_at: str = None, deleted_at: str = None, commit: bool=False):
    deposit = Deposit(user_id=user_id, merchant_id=merchant_id, gl_id=gl_id, account_id=account_id, amount=amount, rate=rate, tenure=tenure, yield_amount=yield_amount, current_value=current_value, withholding_tax=withholding_tax, vat=vat, receiving_account_principal_id=receiving_account_principal_id, receiving_account_interest_id=receiving_account_interest_id, rollover_principal=rollover_principal, rollover_interest=rollover_interest, rollover_at_maturity=rollover_at_maturity, liquidation_charge=liquidation_charge, rollover_count=rollover_count, paid_interest_status=paid_interest_status, status=status, meta_data=meta_data, created_by=created_by, authorized_by=authorized_by, matured_at=matured_at, liquidated_at=liquidated_at, authorized_at=authorized_at, rollover_at=rollover_at, deleted_at=deleted_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(deposit)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(deposit)
    return deposit

def update_deposit(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Deposit).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_deposit(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Deposit).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_deposit(db: Session, id: int=0, commit: bool=False):
    db.query(Deposit).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_deposit_by_id(db: Session, id: int=0):
    return db.query(Deposit).filter_by(id = id).first()

def get_deposits(db: Session, filters: Dict={}):
    query = db.query(Deposit)
    if 'user_id' in filters:
        query = query.filter_by(user_id = filters['user_id'])
    if 'merchant_id' in filters:
        query = query.filter_by(merchant_id = filters['merchant_id'])
    if 'gl_id' in filters:
        query = query.filter_by(gl_id = filters['gl_id'])
    if 'account_id' in filters:
        query = query.filter_by(account_id = filters['account_id'])
    return query.order_by(desc(Deposit.created_at))
