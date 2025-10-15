from typing import Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from database.custom_types import JSONText
from sqlalchemy.orm import relationship


class InvoiceRequest(Base):

    __tablename__ = "invoice_requests"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    product_id = Column(BigInteger, ForeignKey('products.id'))
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    preferred_date_time = Column(String, nullable=True)
    location = Column(String, nullable=True)
    budget_range = Column(String, nullable=True)
    files_meta_data = Column(JSONText)
    status = Column(SmallInteger, default=0)
    approved_by = Column(BigInteger, default=0)
    approved_at = Column(TIMESTAMP(timezone=True), nullable=True)
    rejected_by = Column(BigInteger, default=0)
    rejection_reason = Column(Text, nullable=True)
    rejected_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    user = relationship("User")
    product = relationship("Product")
    invoice = relationship("Invoice", back_populates="invoice_request", uselist=False)
    messages = relationship('Message', back_populates='invoice_request', foreign_keys='Message.invoice_request_id')

def create_invoice_request(db: Session, user_id: int = 0, product_id: int = 0, description: str = None, notes: str = None, preferred_date_time: str = None, location: str = None, budget_range: str = None, files_meta_data: Any = None, status: int = 0, approved_by: int = 0, approved_at: str = None, rejected_by: int = 0, rejection_reason: str = None, rejected_at: str = None, commit: bool=False):
    inv_req = InvoiceRequest(user_id=user_id, product_id=product_id, description=description, notes=notes, preferred_date_time=preferred_date_time, location=location, budget_range=budget_range, files_meta_data=files_meta_data, status=status, approved_by=approved_by, approved_at=approved_at, rejected_by=rejected_by, rejection_reason=rejection_reason, rejected_at=rejected_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(inv_req)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(inv_req)
    return inv_req

def update_invoice_request(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(InvoiceRequest).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_invoice_request(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(InvoiceRequest).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_invoice_request(db: Session, id: int=0, commit: bool=False):
    db.query(InvoiceRequest).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_invoice_request_by_id(db: Session, id: int=0):
    return db.query(InvoiceRequest).filter_by(id = id).first()

def get_invoice_requests(db: Session, filters: Dict={}):
    query = db.query(InvoiceRequest)
    if 'user_id' in filters:
        query = query.filter_by(user_id = filters['user_id'])
    if 'product_id' in filters:
        query = query.filter_by(product_id = filters['product_id'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(InvoiceRequest.created_at))

