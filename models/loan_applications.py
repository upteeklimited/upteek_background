from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class LoanApplication(Base):

    __tablename__ = "loan_applications"
     
    id = Column(BigInteger, primary_key=True, index=True)
    product_id = Column(BigInteger, ForeignKey("financial_products.id"))
    user_id = Column(BigInteger, default=0)
    merchant_id = Column(BigInteger, default=0)
    account_id = Column(BigInteger, default=0)
    card_id = Column(BigInteger, default=0)
    amount = Column(Float, default=0)
    interest_amount = Column(Float, default=0)
    total_amount = Column(Float, default=0)
    top_up_amount = Column(Float, default=0)
    top_up_interest_amount = Column(Float, default=0)
    top_up_total_amount = Column(Float, default=0)
    purpose = Column(Text, nullable=True)
    tenure = Column(Integer, default=0)
    interest_rate = Column(Float, default=0)
    moratorium = Column(Integer, default=0)
    amount_after_moratorium = Column(Float, default=0)
    insurance = Column(Float, default=0)
    management_fee = Column(Float, default=0)
    loan_form_fee = Column(Float, default=0)
    loan_repayment_frequency = Column(Integer, default=0)
    loan_savings_amount = Column(Float, default=0)
    loan_frequency_of_collection = Column(Integer, default=0)
    installment_type = Column(Integer, default=0)
    schedule_type = Column(Integer, default=0)
    loan_data = Column(Text, nullable=True)
    character_data = Column(Text, nullable=True)
    capacity_data = Column(Text, nullable=True)
    capital_data = Column(Text, nullable=True)
    collateral_data = Column(Text, nullable=True)
    condition_data = Column(Text, nullable=True)
    payment_data = Column(Text, nullable=True)
    approval_level = Column(Integer, default=0)
    decline_reason = Column(Text, nullable=True)
    top_up_status = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    authorized_by = Column(BigInteger, default=0)
    authorized_at = Column(TIMESTAMP(timezone=True), nullable=True)
    last_collected_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    financial_product = relationship('FinancialProduct', back_populates='loan_applications', uselist=False)
    loan = relationship('Loan', back_populates='application', foreign_keys='Loan.application_id', uselist=False)

def create_loan_application(db: Session, product_id: int = 0, user_id: int = 0, merchant_id: int = 0, account_id: int = 0, card_id: int = 0, amount: float = 0, interest_amount: float = 0, total_amount: float = 0, top_up_amount: float = 0, top_up_interest_amount: float = 0, top_up_total_amount: float = 0, purpose: str = None, tenure: int = 0, interest_rate: float = 0, moratorium: int = 0, amount_after_moratorium: float = 0, insurance: float = 0, management_fee: float = 0, loan_form_fee: float = 0, loan_repayment_frequency: int = 0, loan_savings_amount: float = 0, loan_frequency_of_collection: int = 0, installment_type: int = 0, schedule_type: int = 0, loan_data: str = None, character_data: str = None, capacity_data: str = None, capital_data: str = None, collateral_data: str = None, condition_data: str = None, payment_data: str = None, approval_level: int = 0, decline_reason: str = None, top_up_status: int = 0, status: int = 0, created_by: int = 0, authorized_by: int = 0, authorized_at: str = None, last_collected_at: str = None, commit: bool=False):
    loan_application = LoanApplication(product_id=product_id, user_id=user_id, merchant_id=merchant_id, account_id=account_id, card_id=card_id, amount=amount, interest_amount=interest_amount, total_amount=total_amount, top_up_amount=top_up_amount, top_up_interest_amount=top_up_interest_amount, top_up_total_amount=top_up_total_amount, purpose=purpose, tenure=tenure, interest_rate=interest_rate, moratorium=moratorium, amount_after_moratorium=amount_after_moratorium, insurance=insurance, management_fee=management_fee, loan_form_fee=loan_form_fee, loan_repayment_frequency=loan_repayment_frequency, loan_savings_amount=loan_savings_amount, loan_frequency_of_collection=loan_frequency_of_collection, installment_type=installment_type, schedule_type=schedule_type, loan_data=loan_data, character_data=character_data, capacity_data=capacity_data, capital_data=capital_data, collateral_data=collateral_data, condition_data=condition_data, payment_data=payment_data, approval_level=approval_level, decline_reason=decline_reason, top_up_status=top_up_status, status=status, created_by=created_by, authorized_by=authorized_by, authorized_at=authorized_at, last_collected_at=last_collected_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(loan_application)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(loan_application)
    return loan_application

def update_loan_application(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(LoanApplication).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_loan_application(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(LoanApplication).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_loan_application(db: Session, id: int=0, commit: bool=False):
    db.query(LoanApplication).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_loan_application_by_id(db: Session, id: int=0):
    return db.query(LoanApplication).filter_by(id = id).first()

def get_loan_applications(db: Session, filters: Dict={}):
    query = db.query(LoanApplication)
    if 'user_id' in filters:
        query = query.filter_by(user_id = filters['user_id'])
    if 'merchant_id' in filters:
        query = query.filter_by(merchant_id = filters['merchant_id'])
    if 'account_id' in filters:
        query = query.filter_by(account_id = filters['account_id'])
    if 'card_id' in filters:
        query = query.filter_by(card_id = filters['card_id'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(LoanApplication.created_at))