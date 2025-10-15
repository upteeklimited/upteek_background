from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class AccountType(Base):

    __tablename__ = "account_types"
     
    id = Column(BigInteger, primary_key=True, index=True)
    product_id = Column(BigInteger, ForeignKey('financial_products.id'))
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    account_code = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    authorized_by = Column(BigInteger, default=0)
    authorized_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    financial_product = relationship('FinancialProduct', back_populates='account_type')
    accounts = relationship('Account', back_populates='account_type')

def create_account_type(db: Session, product_id: int = 0, name: str = None, description: str = None, account_code: str = None, status: int = 0, created_by: int = 0, authorized_by: int = 0, authorized_at: str = None, commit: bool=False):
    account_type = AccountType(product_id=product_id, name=name, description=description, account_code=account_code, status=status, created_by=created_by, authorized_by=authorized_by, authorized_at=authorized_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(account_type)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(account_type)
    return account_type

def update_account_type(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(AccountType).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_account_type(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(AccountType).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_account_type(db: Session, id: int=0, commit: bool=False):
    db.query(AccountType).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_account_type_by_id(db: Session, id: int=0):
    return db.query(AccountType).filter_by(id = id).first()

def get_last_account_type(db: Session):
    return db.query(AccountType).order_by(desc(AccountType.id)).first()

def get_single_account_type_by_product_id(db: Session, product_id: int=0):
    return db.query(AccountType).filter_by(product_id = product_id).first()

def get_single_account_type_by_account_code(db: Session, account_code: str=None):
    return db.query(AccountType).filter_by(account_code = account_code).first()

def get_account_types(db: Session, filters: Dict={}):
    query = db.query(AccountType)
    if 'product_id' in filters:
        query = query.filter_by(product_id = filters['product_id'])
    return query.order_by(desc(AccountType.created_at))