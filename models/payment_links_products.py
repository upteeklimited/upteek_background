from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class PaymentLinkProduct(Base):

    __tablename__ = "payment_links_products"
     
    id = Column(BigInteger, primary_key=True, index=True)
    payment_link_id = Column(BigInteger, ForeignKey('payment_links.id'))
    product_id = Column(BigInteger, ForeignKey('products.id'))
    quantity = Column(Integer, default=0)
    extra_quantity = Column(Integer, default=0)
    amount = Column(Float, default=0)
    meta_data = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    payment_link = relationship("PaymentLink", back_populates="products")
    product = relationship("Product", back_populates="paymentlink_products")

def create_payment_link_product(db: Session, payment_link_id: int = 0, product_id: int = 0, quantity: int = 0, extra_quantity: int = 0, amount: float = 0, meta_data: str = None, status: int = 0, commit: bool=False):
    pay_link_prod = PaymentLinkProduct(payment_link_id=payment_link_id, product_id=product_id, quantity=quantity, extra_quantity=extra_quantity, amount=amount, meta_data=meta_data, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(pay_link_prod)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(pay_link_prod)
    return pay_link_prod

def update_payment_link_product(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(PaymentLinkProduct).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_payment_link_product(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(PaymentLinkProduct).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_payment_link_product(db: Session, id: int=0, commit: bool=False):
    db.query(PaymentLinkProduct).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_payment_link_product_by_id(db: Session, id: int=0):
    return db.query(PaymentLinkProduct).filter_by(id = id).first()

def get_payment_links_products(db: Session, filters: Dict={}):
    query = db.query(PaymentLinkProduct)
    if 'payment_link_id' in filters:
        query = query.filter_by(payment_link_id = filters['payment_link_id'])
    if 'product_id' in filters:
        query = query.filter_by(product_id = filters['product_id'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(PaymentLinkProduct.created_at))

