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


class Conversation(Base):

    __tablename__ = "conversations"
     
    id = Column(BigInteger, primary_key=True, index=True)
    initial_sender_user_id = Column(BigInteger, default=0)
    initial_sender_merchant_id = Column(BigInteger, default=0)
    initial_receiver_user_id = Column(BigInteger, default=0)
    initial_receiver_merchant_id = Column(BigInteger, default=0)
    last_message_id = Column(BigInteger, default=0)
    reference = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_conversation(db: Session, initial_sender_user_id: int = 0, initial_sender_merchant_id: int = 0, initial_receiver_user_id: int = 0, initial_receiver_merchant_id: int = 0, last_message_id: int = 0, reference: str = None, status: int = 0, commit: bool=False):
    conversation = Conversation(initial_sender_user_id=initial_sender_user_id, initial_sender_merchant_id=initial_sender_merchant_id, initial_receiver_user_id=initial_receiver_user_id, initial_receiver_merchant_id=initial_receiver_merchant_id, last_message_id=last_message_id, reference=reference, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(conversation)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(conversation)
    return conversation

def update_conversation(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Conversation).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_conversation(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Conversation).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_conversation(db: Session, id: int=0, commit: bool=False):
    db.query(Conversation).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_conversation_by_id(db: Session, id: int=0):
    return db.query(Conversation).filter_by(id = id).first()

def get_all_conversations(db: Session, filters: Dict={}):
    query = db.query(Conversation)
    if 'initial_sender_user_id' in filters:
        query = query.filter_by(initial_sender_user_id = filters['initial_sender_user_id'])
    if 'initial_sender_merchant_id' in filters:
        query = query.filter_by(initial_sender_merchant_id = filters['initial_sender_merchant_id'])
    if 'initial_receiver_user_id' in filters:
        query = query.filter_by(initial_receiver_user_id = filters['initial_receiver_user_id'])
    if 'initial_receiver_merchant_id' in filters:
        query = query.filter_by(initial_receiver_merchant_id = filters['initial_receiver_merchant_id'])
    if 'last_message_id' in filters:
        query = query.filter_by(last_message_id = filters['last_message_id'])
    if 'reference' in filters:
        query = query.filter_by(reference = filters['reference'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(Conversation.created_at))
