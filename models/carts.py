from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Cart(Base):

    __tablename__ = "carts"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    reference = Column(String, nullable=True)
    total_amount = Column(Float, default=0)
    status = Column(SmallInteger, default=0)
    meta_data = Column(Text, nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    cart_products = relationship("CartProduct", back_populates="cart")


def create_cart(db: Session, user_id: int = 0, reference: str = None, total_amount: float = 0, status: int = 0, meta_data: str = None, commit: bool=False):
    cart = Cart(user_id=user_id, reference=reference, total_amount=total_amount, status=status, meta_data=meta_data, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(cart)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(cart)
    return cart

def update_cart(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Cart).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_cart(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Cart).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_cart(db: Session, id: int=0, commit: bool=False):
    db.query(Cart).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_cart_by_id(db: Session, id: int=0):
    return db.query(Cart).filter_by(id = id).first()

def get_carts(db: Session, filters: Dict={}):
    query = db.query(Cart)
    if 'user_id' in filters:
        query = query.filter_by(user_id = filters['user_id'])
    if 'reference' in filters:
        query = query.filter_by(reference = filters['reference'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(Cart.created_at))
