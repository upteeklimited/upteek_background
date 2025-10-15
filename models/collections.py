from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Collection(Base):

    __tablename__ = "collections"
     
    id = Column(BigInteger, primary_key=True, index=True)
    loan_id = Column(BigInteger, ForeignKey("loans.id"))
    amount = Column(Float, default=0)
    total_principal = Column(Float, default=0)
    total_interest = Column(Float, default=0)
    bal_principal = Column(Float, default=0)
    bal_interest = Column(Float, default=0)
    retrial_num = Column(Integer, default=0)
    retrial_status = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    collected_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    loan = relationship('Loan', back_populates='collections', uselist=False)

def create_collection(db: Session, loan_id: int = 0, amount: float = 0, total_principal: float = 0, total_interest: float = 0, bal_principal: float = 0, bal_interest: float = 0, retrial_num: int = 0, status: int = 0, retrial_status: str = None, collected_at: str = None, deleted_at: str = None, commit: bool=False):
    collection = Collection(loan_id=loan_id, amount=amount, total_principal=total_principal, total_interest=total_interest, bal_principal=bal_principal, bal_interest=bal_interest, retrial_num=retrial_num, status=status, retrial_status=retrial_status, collected_at=collected_at, deleted_at=deleted_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(collection)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(collection)
    return collection

def update_collection(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Collection).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_collection(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Collection).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_collection(db: Session, id: int=0, commit: bool=False):
    db.query(Collection).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_collection_by_id(db: Session, id: int=0):
    return db.query(Collection).filter_by(id = id).first()

def get_collections(db: Session, filters: Dict={}):
    query = db.query(Collection)
    if 'loan_id' in filters:
        query = query.filter_by(loan_id = filters['loan_id'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(Collection.created_at))