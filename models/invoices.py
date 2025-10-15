from typing import Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from database.custom_types import JSONText
from sqlalchemy.orm import relationship


class Invoice(Base):

    __tablename__ = "invoices"
     
    id = Column(BigInteger, primary_key=True, index=True)
    currency_id = Column(BigInteger, ForeignKey('currencies.id'))
    invoice_request_id = Column(BigInteger, ForeignKey('invoice_requests.id'))
    user_id = Column(BigInteger, ForeignKey('users.id'))
    merchant_id = Column(BigInteger, ForeignKey('merchants.id'))
    product_id = Column(BigInteger, ForeignKey('products.id'))
    customer_email = Column(String, nullable=True)
    customer_phone_number = Column(String, nullable=True)
    customer_full_name = Column(String, nullable=True)
    customer_address = Column(String, nullable=True)
    reference = Column(String, nullable=True)
    url = Column(String, nullable=True)
    title = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    due_date = Column(Text, nullable=True)
    tax = Column(Float, default=0)
    vat = Column(Float, default=0)
    wht = Column(Float, default=0)
    discount_amount = Column(Float, default=0)
    shipping_fee = Column(Float, default=0)
    total_amount = Column(Float, default=0)
    payment_date = Column(Text, nullable=True)
    payment_method = Column(Text, nullable=True)
    is_paid = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    paid_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    currency = relationship('Currency')
    user = relationship('User')
    merchant = relationship('Merchant')
    product = relationship('Product')
    invoice_request = relationship("InvoiceRequest", back_populates="invoice")
    order = relationship("Order", back_populates="invoice")
    items = relationship("InvoiceItem", back_populates="invoice", foreign_keys='InvoiceItem.invoice_id', uselist=True)
    messages = relationship('Message', back_populates='invoice', foreign_keys='Message.invoice_id')

def create_invoice(db: Session, currency_id: int = 0, invoice_request_id: int = 0, user_id: int = 0, merchant_id: int = 0, product_id: int = 0, customer_email: str = None, customer_phone_number: str = None, customer_full_name: str = None, customer_address: str = None, reference: str = None, url: str = None, title: str = None, description: str = None, notes: str = None, due_date: str = None, tax: float = 0, vat: float = 0, wht: float = 0, discount_amount: float = 0, shipping_fee: float = 0, total_amount: float = 0, payment_date: str = None, is_paid: int = 0, status: int = 0, paid_at: str = None, commit: bool=False):
    inv = Invoice(currency_id=currency_id, invoice_request_id=invoice_request_id, user_id=user_id, merchant_id=merchant_id, product_id=product_id, customer_email=customer_email, customer_phone_number=customer_phone_number, customer_full_name=customer_full_name, customer_address=customer_address, reference=reference, url=url, title=title, description=description, notes=notes, due_date=due_date, tax=tax, vat=vat, wht=wht, discount_amount=discount_amount, shipping_fee=shipping_fee, total_amount=total_amount, payment_date=payment_date, is_paid=is_paid, paid_at=paid_at, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(inv)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(inv)
    return inv

def update_invoice(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Invoice).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_invoice(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Invoice).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_invoice(db: Session, id: int=0, commit: bool=False):
    db.query(Invoice).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_invoice_by_id(db: Session, id: int=0):
    return db.query(Invoice).filter_by(id = id).first()

def get_invoices(db: Session, filters: Dict={}):
    query = db.query(Invoice)
    if 'currency_id' in filters:
        query = query.filter_by(currency_id = filters['currency_id'])
    if 'invoice_request_id' in filters:
        query = query.filter_by(invoice_request_id = filters['invoice_request_id'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(Invoice.created_at))

