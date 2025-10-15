from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class TransactionType(Base):

    __tablename__ = "transaction_types"
     
    id = Column(BigInteger, primary_key=True, index=True)
    corresponding_gl_id = Column(BigInteger, default=0)
    charge_gl_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    code = Column(String, nullable=True)
    action = Column(Integer, default=0)
    chargeable = Column(Integer, default=0)
    charge_type = Column(Integer, default=0)
    charge_percentage = Column(Float, default=0)
    charge_flat = Column(Float, default=0)
    charge_flatmax_amount = Column(Float, default=0)
    min_amount = Column(Float, default=0)
    max_amount = Column(Float, default=0)
    require_approval = Column(SmallInteger, default=0)
    require_approval_amount = Column(Float, default=0)
    is_system = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    authorized_by = Column(BigInteger, default=0)
    authorized_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    transactions = relationship('Transaction', back_populates='transaction_type', foreign_keys='Transaction.type_id')

def create_transaction_type(db: Session, corresponding_gl_id: int = 0, charge_gl_id: int = 0, name: str = None, description: str = None, code: str = None, action: int = 0, chargeable: int = 0, charge_type: int = 0, charge_percentage: float = 0, charge_flat: float = 0, charge_flatmax_amount: float = 0, min_amount: float = 0, max_amount: float = 0, require_approval: int = 0, require_approval_amount: float = 0, is_system: int = 0, status: int = 0, created_by: int = 0, authorized_by: int = 0, authorized_at: str = None, commit: bool=False):
    transaction_type = TransactionType(corresponding_gl_id=corresponding_gl_id, charge_gl_id=charge_gl_id, name=name, description=description, code=code, action=action, chargeable=chargeable, charge_type=charge_type, charge_percentage=charge_percentage, charge_flat=charge_flat, charge_flatmax_amount=charge_flatmax_amount, min_amount=min_amount, max_amount=max_amount, require_approval=require_approval, require_approval_amount=require_approval_amount, is_system=is_system, status=status, created_by=created_by, authorized_by=authorized_by, authorized_at=authorized_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(transaction_type)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(transaction_type)
    return transaction_type

def update_transaction_type(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(TransactionType).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_transaction_type(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(TransactionType).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_transaction_type(db: Session, id: int=0, commit: bool=False):
    db.query(TransactionType).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_transaction_type_by_id(db: Session, id: int=0):
    return db.query(TransactionType).filter_by(id = id).first()

def get_single_transaction_type_by_code(db: Session, code: str=None):
    return db.query(TransactionType).filter_by(code = code).first()

def get_last_transaction_type(db: Session):
    return db.query(TransactionType).order_by(desc(TransactionType.id)).first()

def get_transaction_types(db: Session, filters: Dict={}):
    query = db.query(TransactionType)
    if 'corresponding_gl_id' in filters:
        query = query.filter_by(corresponding_gl_id = filters['corresponding_gl_id'])
    if 'charge_gl_id' in filters:
        query = query.filter_by(charge_gl_id = filters['charge_gl_id'])
    if 'name' in filters:
        query = query.filter(TransactionType.name.like('%' + filters['name'] + '%'))
    if 'code' in filters:
        query = query.filter(TransactionType.code.like('%' + filters['code'] + '%'))
    if 'action' in filters:
        query = query.filter_by(action = filters['action'])
    if 'chargeable' in filters:
        query = query.filter_by(chargeable = filters['chargeable'])
    if 'charge_type' in filters:
        query = query.filter_by(charge_type = filters['charge_type'])
    if 'require_approval' in filters:
        query = query.filter_by(require_approval = filters['require_approval'])
    if 'is_system' in filters:
        query = query.filter_by(is_system = filters['is_system'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    if 'created_by' in filters:
        query = query.filter_by(created_by = filters['created_by'])
    return query.order_by(desc(TransactionType.created_at))

