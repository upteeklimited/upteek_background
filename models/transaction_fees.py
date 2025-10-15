from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class TransactionFee(Base):

    __tablename__ = "transaction_fees"
     
    id = Column(BigInteger, primary_key=True, index=True)
    transaction_type_id = Column(BigInteger, default=0)
    from_amount = Column(Float, default=0)
    to_amount = Column(Float, default=0)
    amount = Column(Float, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_transaction_fee(db: Session, transaction_type_id: int = 0, from_amount: float = 0, to_amount: float = 0, amount: float = 0, status: int = 0, commit: bool=False):
    transaction_fee = TransactionFee(transaction_type_id=transaction_type_id, from_amount=from_amount, to_amount=to_amount, amount=amount, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(transaction_fee)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(transaction_fee)
    return transaction_fee

def update_transaction_fee(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(TransactionFee).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_transaction_fee(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(TransactionFee).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_transaction_fee(db: Session, id: int=0, commit: bool=False):
    db.query(TransactionFee).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_all_transaction_fees(db: Session, filters: Dict={}):
    query = db.query(TransactionFee)
    if 'transaction_type_id' in filters:
        query = query.filter_by(transaction_type_id = filters['transaction_type_id'])
    return query.order_by(desc(TransactionFee.created_at))