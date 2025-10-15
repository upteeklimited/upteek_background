from typing import Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from database.custom_types import JSONText
from sqlalchemy.orm import relationship


class OrderLog(Base):

    __tablename__ = "order_logs"
     
    id = Column(BigInteger, primary_key=True, index=True)
    order_id = Column(BigInteger, default=0)
    event_type = Column(Integer, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_order_log(db: Session, order_id: int = 0, event_type: int = 0, status: int = 0, commit: bool=False):
    ord_log = OrderLog(order_id=order_id, event_type=event_type, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(ord_log)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(ord_log)
    return ord_log

def update_order_log(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(OrderLog).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_order_log(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(OrderLog).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_order_log(db: Session, id: int=0, commit: bool=False):
    db.query(OrderLog).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_order_log_by_id(db: Session, id: int=0):
    return db.query(OrderLog).filter_by(id = id).first()

def get_order_logs(db: Session, filters: Dict={}):
    query = db.query(OrderLog)
    if 'order_id' in filters:
        query = query.filter_by(order_id = filters['order_id'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(OrderLog.created_at))

