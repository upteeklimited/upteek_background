from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class CartProduct(Base):

    __tablename__ = "carts_products"
     
    id = Column(BigInteger, primary_key=True, index=True)
    product_id = Column(BigInteger, ForeignKey('products.id'))
    cart_id = Column(BigInteger, ForeignKey('carts.id'))
    quantity = Column(Integer, default=0)
    extra_quantity = Column(Integer, default=0)
    amount = Column(Float, default=0)
    meta_data = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    cart = relationship("Cart", back_populates="cart_products")
    product = relationship("Product", back_populates="cart_products")

def create_cart_product(db: Session, product_id: int = 0, cart_id: int = 0, quantity: int = 0, extra_quantity: int = 0, amount: float = 0, meta_data: str = None, status: int = 0, commit: bool=False):
    cart_product = CartProduct(product_id=product_id, cart_id=cart_id, quantity=quantity, extra_quantity=extra_quantity, amount=amount, meta_data=meta_data, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(cart_product)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(cart_product)
    return cart_product

def update_cart_product(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(CartProduct).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_cart_product(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(CartProduct).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_cart_product(db: Session, id: int=0, commit: bool=False):
    db.query(CartProduct).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_all_carts_products(db: Session, filters: Dict={}):
    query = db.query(CartProduct)
    if 'product_id' in filters:
        query = query.filter_by(product_id = filters['product_id'])
    if 'cart_id' in filters:
        query = query.filter_by(cart_id = filters['cart_id'])
    return query.order_by(desc(CartProduct.created_at))
