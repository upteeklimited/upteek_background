from typing import Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from database.custom_types import JSONText
from sqlalchemy.orm import relationship


class InvoiceItem(Base):

    __tablename__ = "invoice_items"
     
    id = Column(BigInteger, primary_key=True, index=True)
    invoice_id = Column(BigInteger, ForeignKey('invoices.id'))
    product_id = Column(BigInteger, ForeignKey('products.id'))
    description = Column(Text, nullable=True)
    amount = Column(Float, default=0)
    quantity = Column(Integer, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    invoice = relationship("Invoice", back_populates="items", foreign_keys=[invoice_id])
    product = relationship('Product')

def create_invoice_item(db: Session, invoice_id: int = 0, product_id: int = 0, description: str = None, amount: float = 0, quantity: int = 0, status: int = 0, commit: bool=False):
    inv_item = InvoiceItem(invoice_id=invoice_id, product_id=product_id, description=description, amount=amount, quantity=quantity, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(inv_item)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(inv_item)
    return inv_item

def update_invoice_item(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(InvoiceItem).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_invoice_item(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(InvoiceItem).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_invoice_item(db: Session, id: int=0, commit: bool=False):
    db.query(InvoiceItem).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_invoice_item_by_id(db: Session, id: int=0):
    return db.query(InvoiceItem).filter_by(id = id).first()

def get_invoice_items(db: Session, filters: Dict={}):
    query = db.query(InvoiceItem)
    if 'invoice_id' in filters:
        query = query.filter_by(invoice_id = filters['invoice_id'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(InvoiceItem.created_at))

