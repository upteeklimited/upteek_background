from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship, foreign
from models.users import User
from models.profiles import Profile
from models.merchants import Merchant
from models.media import Medium
from models.invoices import Invoice


class Message(Base):

    __tablename__ = "messages"
     
    id = Column(BigInteger, primary_key=True, index=True)
    conversation_id = Column(BigInteger, default=0)
    sender_user_id = Column(BigInteger, default=0)
    receiver_user_id = Column(BigInteger, default=0)
    previous_message_id = Column(BigInteger, default=0)
    parent_id = Column(BigInteger, default=0)
    invoice_request_id = Column(BigInteger, ForeignKey('invoice_requests.id'))
    invoice_id = Column(BigInteger, ForeignKey('invoices.id'))
    reference = Column(String, nullable=True)
    title = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    attached_file = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    media = relationship(
        "Medium",
        primaryjoin=lambda: and_(
            foreign(Medium.mediumable_id) == Message.id,
            Medium.mediumable_type == 'message'
        ),
        viewonly=True
    )
    invoice_request = relationship("InvoiceRequest", back_populates='messages', foreign_keys=[invoice_request_id])
    invoice = relationship("Invoice", back_populates='messages', foreign_keys=[invoice_id])

def create_message(db: Session, conversation_id: int = 0, sender_user_id: int = 0, receiver_user_id: int = 0, previous_message_id: int = 0, parent_id: int = 0, invoice_request_id: int = 0, invoice_id: int = 0, reference: str = None, title: str = None, body: str = None, attached_file: str = None, status: int = 0, commit: bool=False):
    message = Message(conversation_id=conversation_id, sender_user_id=sender_user_id, receiver_user_id=receiver_user_id, previous_message_id=previous_message_id, parent_id=parent_id, invoice_request_id=invoice_request_id, invoice_id=invoice_id, reference=reference, title=title, body=body, attached_file=attached_file, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(message)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(message)
    return message

def update_message(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Message).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_message(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Message).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_message(db: Session, id: int=0, commit: bool=False):
    db.query(Message).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_all_messages(db: Session, filters: Dict={}):
    query = db.query(Message)
    if 'conversation_id' in filters:
        query = query.filter_by(conversation_id = filters['conversation_id'])
    if 'reference' in filters:
        query = query.filter_by(reference = filters['reference'])
    if 'sender_user_id' in filters:
        query = query.filter_by(sender_user_id = filters['sender_user_id'])
    if 'receiver_user_id' in filters:
        query = query.filter_by(receiver_user_id = filters['receiver_user_id'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(Message.created_at))
