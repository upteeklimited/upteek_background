from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Statement_Header(Base):

    __tablename__ = "statement_headers"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, default=0)
    account_id = Column(BigInteger, default=0)
    reference = Column(String, nullable=True)
    opening_balance = Column(Float, default=0)
    closing_balance = Column(Float, default=0)
    file_path = Column(String, nullable=True)
    is_sent = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_statement_header(db: Session, user_id: int = 0, account_id: int = 0, reference: str = None, opening_balance: float = 0, closing_balance: float = 0, file_path: str = None, is_sent: int = 0, status: int = 0, commit: bool=False):
    sh = Statement_Header(user_id=user_id, account_id=account_id, reference=reference, opening_balance=opening_balance, closing_balance=closing_balance, file_path=file_path, is_sent=is_sent, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(sh)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(sh)
    return sh

def update_statement_header(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Statement_Header).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_statement_header(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Statement_Header).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_statement_header(db: Session, id: int=0, commit: bool=False):
    db.query(Statement_Header).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_statement_header_by_id(db: Session, id: int=0):
    return db.query(Statement_Header).filter_by(id = id).first()

def get_statement_headers(db: Session, filters: Dict={}):
    query = db.query(Statement_Header)
    if 'user_id' in filters:
        query = query.filter_by(user_id = filters['user_id'])
    if 'account_id' in filters:
        query = query.filter_by(account_id = filters['account_id'])
    if 'reference' in filters:
        query = query.filter(Statement_Header.reference.like("%" + filters['reference'] + "%"))
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(Statement_Header.created_at))