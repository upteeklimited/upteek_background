from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Card(Base):

    __tablename__ = "cards"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, default=0)
    provider = Column(String, nullable=True)
    external_reference = Column(String, nullable=True)
    external_email = Column(String, nullable=True)
    card_type = Column(String, nullable=True)
    card_bank = Column(String, nullable=True)
    last_four_digits = Column(String, nullable=True)
    card_expiry = Column(String, nullable=True)
    meta_data = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_card(db: Session, user_id: int = 0, provider: str = None, external_reference: str = None, external_email: str = None, card_type: str = None, card_bank: str = None, last_four_digits: str = None, card_expiry: str = None, meta_data: str = None, status: int = 0, deleted_at: str = None, commit: bool=False):
    card = Card(user_id=user_id, provider=provider, external_reference=external_reference, external_email=external_email, card_type=card_type, card_bank=card_bank, last_four_digits=last_four_digits, card_expiry=card_expiry, meta_data=meta_data, status=status, deleted_at=deleted_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(card)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(card)
    return card

def update_card(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Card).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_card(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Card).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_card(db: Session, id: int=0, commit: bool=False):
    db.query(Card).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_card_by_id(db: Session, id: int=0):
    return db.query(Card).filter_by(id = id).first()

def get_cards(db: Session, filters: Dict={}):
    query = db.query(Card)
    if 'user_id' in filters:
        query = query.filter_by(user_id = filters['user_id'])
    if 'provider' in filters:
        query = query.filter_by(provider = filters['provider'])
    return query.order_by(desc(Card.created_at))