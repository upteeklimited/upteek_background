from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Loan(Base):

    __tablename__ = "loans"
     
    id = Column(BigInteger, primary_key=True, index=True)
    application_id = Column(BigInteger, ForeignKey("loan_applications.id"))
    user_id = Column(BigInteger, default=0)
    merchant_id = Column(BigInteger, default=0)
    account_id = Column(BigInteger, default=0)
    loan_account_id = Column(BigInteger, default=0)
    gl_account_id = Column(BigInteger, default=0)
    restructured_application_id = Column(BigInteger, default=0)
    card_id = Column(BigInteger, default=0)
    amount = Column(Float, default=0)
    unpaid_principal = Column(Float, default=0)
    unearned_interest = Column(Float, default=0)
    is_paid = Column(SmallInteger, default=0)
    is_provisioned = Column(SmallInteger, default=0)
    is_restructured = Column(SmallInteger, default=0)
    is_write_off = Column(SmallInteger, default=0)
    meta_data = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    past_due_at = Column(TIMESTAMP(timezone=True), nullable=True)
    doubtful_at = Column(TIMESTAMP(timezone=True), nullable=True)
    substandard_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deliquent_at = Column(TIMESTAMP(timezone=True), nullable=True)
    provisioned_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    application = relationship('LoanApplication', back_populates='loan', uselist=False)
    collections = relationship('Collection', back_populates='loan', foreign_keys='Collection.loan_id', uselist=True)

def create_loan(db: Session, application_id: int = 0, user_id: int = 0, merchant_id: int = 0, account_id: int = 0, loan_account_id: int = 0, gl_account_id: int = 0, restructured_application_id: int = 0, card_id: int = 0, amount: float = 0, unpaid_principal: float = 0, unearned_interest: float = 0, is_paid: int = 0, is_provisioned: int = 0, is_restructured: int = 0, is_write_off: int = 0, meta_data: str = None, status: int = 0, past_due_at: str = None, doubtful_at: str = None, substandard_at: str = None, deliquent_at: str = None, provisioned_at: str = None, deleted_at: str = None, commit: bool=False):
    loan = Loan(application_id=application_id, user_id=user_id, merchant_id=merchant_id, account_id=account_id, loan_account_id=loan_account_id, gl_account_id=gl_account_id, restructured_application_id=restructured_application_id, card_id=card_id, amount=amount, unpaid_principal=unpaid_principal, unearned_interest=unearned_interest, is_paid=is_paid, is_provisioned=is_provisioned, is_restructured=is_restructured, is_write_off=is_write_off, meta_data=meta_data, status=status, past_due_at=past_due_at, doubtful_at=doubtful_at, substandard_at=substandard_at, deliquent_at=deliquent_at, provisioned_at=provisioned_at, deleted_at=deleted_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(loan)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(loan)
    return loan

def update_loan(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Loan).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_loan(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Loan).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_loan(db: Session, id: int=0, commit: bool=False):
    db.query(Loan).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_loan_by_id(db: Session, id: int=0):
    return db.query(Loan).filter_by(id = id).first()

def get_loans(db: Session, filters: Dict={}):
    query = db.query(Loan)
    if 'user_id' in filters:
        query = query.filter_by(user_id = filters['user_id'])
    if 'application_id' in filters:
        query = query.filter_by(application_id = filters['application_id'])
    if 'merchant_id' in filters:
        query = query.filter_by(merchant_id = filters['merchant_id'])
    if 'account_id' in filters:
        query = query.filter_by(account_id = filters['account_id'])
    if 'loan_account_id' in filters:
        query = query.filter_by(loan_account_id = filters['loan_account_id'])
    if 'gl_account_id' in filters:
        query = query.filter_by(gl_account_id = filters['gl_account_id'])
    if 'restructured_application_id' in filters:
        query = query.filter_by(restructured_application_id = filters['restructured_application_id'])
    if 'card_id' in filters:
        query = query.filter_by(card_id = filters['card_id'])
    return query.order_by(desc(Loan.created_at))