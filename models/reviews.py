from typing import Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from database.custom_types import JSONText
from sqlalchemy.orm import relationship


class Review(Base):

    __tablename__ = "reviews"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    merchant_id = Column(BigInteger, default=0)
    product_id = Column(BigInteger, default=0)
    reviewable_id = Column(BigInteger, default=0)
    reviewable_type = Column(String, nullable=True)
    title = Column(String, nullable=True)
    data_value = Column(Text, nullable=True)
    body = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    user = relationship('User', back_populates='reviews')

def create_review(db: Session, user_id: int = 0, merchant_id: int = 0, product_id: int = 0, reviewable_id: int = 0, reviewable_type: str = None, title: str = None, data_value: str = None, body: str = None, status: int = 0, commit: bool=False):
    review = Review(user_id=user_id, merchant_id=merchant_id, product_id=product_id, reviewable_id=reviewable_id, reviewable_type=reviewable_type, title=title, data_value=data_value, body=body, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(review)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(review)
    return review

def update_review(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Review).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_review(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Review).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_review(db: Session, id: int=0, commit: bool=False):
    db.query(Review).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_review_by_id(db: Session, id: int=0):
    return db.query(Review).filter_by(id = id).first()

def get_reviews(db: Session, filters: Dict={}):
    query = db.query(Review)
    if 'user_id' in filters:
        query = query.filter_by(user_id = filters['user_id'])
    if 'merchant_id' in filters:
        query = query.filter_by(merchant_id = filters['merchant_id'])
    if 'product_id' in filters:
        query = query.filter_by(product_id = filters['product_id'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(Review.created_at))

