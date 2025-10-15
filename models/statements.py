from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Statement(Base):

    __tablename__ = "statements"
     
    id = Column(BigInteger, primary_key=True, index=True)
    header_id = Column(BigInteger, default=0)
    transaction_id = Column(BigInteger, default=0)
    amount_debit = Column(Float, default=0)
    amount_credit = Column(Float, default=0)
    balance = Column(Float, default=0)
    value_date = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_statement(db: Session, header_id: int = 0, transaction_id: int = 0, amount_debit: float = 0, amount_credit: float = 0, balance: float = 0, value_date: str = None, status: int = 0, commit: bool=False):
    st = Statement(header_id=header_id, transaction_id=transaction_id, amount_debit=amount_debit, amount_credit=amount_credit, balance=balance, value_date=value_date, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(st)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(st)
    return st

def update_statement(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Statement).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_statement(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Statement).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_statement(db: Session, id: int=0, commit: bool=False):
    db.query(Statement).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_statement_by_id(db: Session, id: int=0):
    return db.query(Statement).filter_by(id = id).first()

def get_statements(db: Session, filters: Dict={}):
    query = db.query(Statement)
    if 'header_id' in filters:
        query = query.filter_by(header_id = filters['header_id'])
    if 'transaction_id' in filters:
        query = query.filter_by(transaction_id = filters['transaction_id'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(Statement.created_at))