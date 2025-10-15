from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class PaymentLink(Base):

    __tablename__ = "payment_links"
     
    id = Column(BigInteger, primary_key=True, index=True)
    merchant_id = Column(BigInteger, ForeignKey('merchants.id'))
    product_id = Column(BigInteger, ForeignKey('products.id'))
    title = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    reference = Column(String, nullable=True)
    url = Column(String, nullable=True)
    amount = Column(Float, default=0)
    items_for_sale = Column(Integer, default=0)
    quantity = Column(Integer, default=0)
    number_of_uses = Column(Integer, default=0)
    status = Column(SmallInteger, default=0)
    paid_at = Column(TIMESTAMP(timezone=True), nullable=True)
    expired_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    order = relationship("Order", back_populates="payment_link")
    merchant = relationship('Merchant', back_populates='payment_links', foreign_keys=[merchant_id])
    product = relationship("Product", back_populates="payment_links")
    products = relationship("PaymentLinkProduct", back_populates="payment_link", uselist=True)

def create_payment_link(db: Session, merchant_id: int = 0, product_id: int = 0, title: str = None, description: str = None, reference: str = None, url: str = None, amount: float = 0, items_for_sale: int = 0, quantity: int = 0, number_of_uses: int = 0, status: int = 0, expired_at: str = None, paid_at: str = None, commit: bool=False):
    pay_link = PaymentLink(merchant_id=merchant_id, product_id=product_id, title=title, description=description, reference=reference, url=url, amount=amount, items_for_sale=items_for_sale, quantity=quantity, number_of_uses=number_of_uses, status=status, paid_at=paid_at, expired_at=expired_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(pay_link)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(pay_link)
    return pay_link

def update_payment_link(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(PaymentLink).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_payment_link(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(PaymentLink).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_payment_link(db: Session, id: int=0, commit: bool=False):
    db.query(PaymentLink).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_payment_link_by_id(db: Session, id: int=0):
    return db.query(PaymentLink).filter_by(id = id).first()

def get_single_payment_link_by_reference(db: Session, reference: str=None):
    return db.query(PaymentLink).filter_by(reference = reference).first()

def get_payment_links(db: Session, filters: Dict={}):
    query = db.query(PaymentLink)
    if 'merchant_id' in filters:
        query = query.filter_by(merchant_id = filters['merchant_id'])
    if 'product_id' in filters:
        query = query.filter_by(product_id = filters['product_id'])
    if 'title' in filters:
        query = query.filter(PaymentLink.title.like('%' + filters['title'] + '%'))
    if 'reference' in filters:
        query = query.filter(PaymentLink.reference.like('%' + filters['reference'] + '%'))
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(PaymentLink.created_at))

