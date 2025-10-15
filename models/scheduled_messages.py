from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class ScheduledMessage(Base):

    __tablename__ = "scheduled_messages"
     
    id = Column(BigInteger, primary_key=True, index=True)
    reference = Column(String, nullable=True)
    receipients = Column(Text, nullable=True)
    title = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    attached_file = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    scheduled_at = Column(TIMESTAMP(timezone=True), nullable=True)
    executed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_scheduled_message(db: Session, reference: str = None, receipients: str = None, title: str = None, body: str = None, attached_file: str = None, status: int = 0, created_by: int = 0, scheduled_at: str = None, executed_at: str = None, commit: bool=False):
    scheduled_message = ScheduledMessage(reference=reference, receipients=receipients, title=title, body=body, attached_file=attached_file, status=status, created_by=created_by, scheduled_at=scheduled_at, executed_at=executed_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(scheduled_message)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(scheduled_message)
    return scheduled_message

def update_scheduled_message(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(ScheduledMessage).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_scheduled_message(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(ScheduledMessage).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_scheduled_message(db: Session, id: int=0, commit: bool=False):
    db.query(ScheduledMessage).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_all_scheduled_messages(db: Session, filters: Dict={}):
    query = db.query(ScheduledMessage)
    if 'reference' in filters:
        query = query.filter_by(reference = filters['reference'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(Message.created_at))

