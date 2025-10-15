from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class FinancialProduct(Base):

    __tablename__ = "financial_products"
     
    id = Column(BigInteger, primary_key=True, index=True)
    country_id = Column(BigInteger, default=0)
    currency_id = Column(BigInteger, default=0)
    gl_id = Column(BigInteger, default=0)
    interest_expense_gl_id = Column(BigInteger, default=0)
    interest_income_gl_id = Column(BigInteger, default=0)
    principal_unpaid_gl_id = Column(BigInteger, default=0)
    interest_unearned_gl_id = Column(BigInteger, default=0)
    fixed_charge_gl_id = Column(BigInteger, default=0)
    insurance_holding_gl_id = Column(BigInteger, default=0)
    overdrawn_interest_gl_id = Column(BigInteger, default=0)
    liability_overdraft_gl_id = Column(BigInteger, default=0)
    interest_receivable_gl_id = Column(BigInteger, default=0)
    interest_payable_gl_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    product_type = Column(Integer, default=0)
    user_type = Column(Integer, default=0)
    individual_compliance_type = Column(Integer, default=0)
    merchant_compliance_type = Column(Integer, default=0)
    interest_rate = Column(Float, default=0)
    overdrawn_interest_rate = Column(Float, default=0)
    charge_if_overdrawn = Column(Float, default=0)
    charges = Column(Float, default=0)
    cot_rate = Column(Float, default=0)
    minimum_amount = Column(Float, default=0)
    maximum_amount = Column(Float, default=0)
    liquidation_penalty = Column(Float, default=0)
    tenure = Column(Integer, default=0)
    interest_tenure_type = Column(Integer, default=0)
    interest_tenure_data = Column(Text, nullable=True)
    guarantor_requirement = Column(SmallInteger, default=0)
    amount_to_require_guarantor = Column(Float, default=0)
    instant_interest_pay_status = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    authorized_by = Column(BigInteger, default=0)
    authorized_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    account_type = relationship('AccountType', back_populates='financial_product', foreign_keys='AccountType.product_id', uselist=False)
    loan_applications = relationship('LoanApplication', back_populates='financial_product', foreign_keys='LoanApplication.product_id', uselist=True)

def create_financial_product(db: Session, country_id: int = 0, currency_id: int = 0, gl_id: int = 0, interest_expense_gl_id: int = 0, interest_income_gl_id: int = 0, principal_unpaid_gl_id: int = 0, interest_unearned_gl_id: int = 0, fixed_charge_gl_id: int = 0, insurance_holding_gl_id: int = 0, overdrawn_interest_gl_id: int = 0, liability_overdraft_gl_id: int = 0, interest_receivable_gl_id: int = 0, interest_payable_gl_id: int = 0, name: str = None, description: str = None, product_type: int = 0, user_type: int = 0, individual_compliance_type: int = 0, merchant_compliance_type: int = 0, interest_rate: float = 0, overdrawn_interest_rate: float = 0, charge_if_overdrawn: float = 0, charges: float = 0, cot_rate: float = 0, minimum_amount: float = 0, maximum_amount: float = 0, liquidation_penalty: float = 0, tenure: int = 0, interest_tenure_type: int = 0, interest_tenure_data: str = None, guarantor_requirement: int = 0, amount_to_require_guarantor: float = 0, instant_interest_pay_status: int = 0, status: int = 0, created_by: int = 0, authorized_by: int = 0, authorized_at: str = None, commit: bool=False):
    financial_product = FinancialProduct(country_id=country_id, currency_id=currency_id, gl_id=gl_id, interest_expense_gl_id=interest_expense_gl_id, interest_income_gl_id=interest_income_gl_id, principal_unpaid_gl_id=principal_unpaid_gl_id, interest_unearned_gl_id=interest_unearned_gl_id, fixed_charge_gl_id=fixed_charge_gl_id, insurance_holding_gl_id=insurance_holding_gl_id, overdrawn_interest_gl_id=overdrawn_interest_gl_id, liability_overdraft_gl_id=liability_overdraft_gl_id, interest_receivable_gl_id=interest_receivable_gl_id, interest_payable_gl_id=interest_payable_gl_id, name=name, description=description, product_type=product_type, user_type=user_type, individual_compliance_type=individual_compliance_type, merchant_compliance_type=merchant_compliance_type, interest_rate=interest_rate, overdrawn_interest_rate=overdrawn_interest_rate, charge_if_overdrawn=charge_if_overdrawn, charges=charges, cot_rate=cot_rate, minimum_amount=minimum_amount, maximum_amount=maximum_amount, liquidation_penalty=liquidation_penalty, tenure=tenure, interest_tenure_type=interest_tenure_type, interest_tenure_data=interest_tenure_data, guarantor_requirement=guarantor_requirement, amount_to_require_guarantor=amount_to_require_guarantor, instant_interest_pay_status=instant_interest_pay_status, status=status, created_by=created_by, authorized_by=authorized_by, authorized_at=authorized_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(financial_product)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(financial_product)
    return financial_product

def update_financial_product(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(FinancialProduct).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_financial_product(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(FinancialProduct).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_financial_product(db: Session, id: int=0, commit: bool=False):
    db.query(FinancialProduct).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_financial_product_by_id(db: Session, id: int=0):
    return db.query(FinancialProduct).filter_by(id = id).first()

def get_financial_products(db: Session, filters: Dict={}):
    query = db.query(FinancialProduct)
    if 'country_id' in filters:
        query = query.filter_by(country_id = filters['country_id'])
    if 'currency_id' in filters:
        query = query.filter_by(currency_id = filters['currency_id'])
    if 'product_type' in filters:
        query = query.filter_by(product_type = filters['product_type'])
    if 'user_type' in filters:
        query = query.filter_by(user_type = filters['user_type'])
    if 'individual_compliance_type' in filters:
        query = query.filter_by(individual_compliance_type = filters['individual_compliance_type'])
    if 'merchant_compliance_type' in filters:
        query = query.filter_by(merchant_compliance_type = filters['merchant_compliance_type'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    if 'name' in filters:
        query = query.filter(FinancialProduct.name.like('%'+filters['name']+'%'))
    return query.order_by(desc(FinancialProduct.created_at))
    