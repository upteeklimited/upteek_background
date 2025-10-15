from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class GroupProduct(Base):

    __tablename__ = "groups_products"
     
    id = Column(BigInteger, primary_key=True, index=True)
    product_id = Column(BigInteger, ForeignKey('products.id'))
    group_id = Column(BigInteger, ForeignKey('groups.id'))
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_group_product(db: Session, product_id: int = 0, group_id: int = 0, status: int = 0, commit: bool=False):
    group_product = GroupProduct(product_id=product_id, group_id=group_id, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(group_product)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(group_product)
    return group_product

def update_group_product(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(GroupProduct).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_group_product(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(GroupProduct).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_group_product(db: Session, id: int=0, commit: bool=False):
    db.query(GroupProduct).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_group_product_by_id(db: Session, id: int=0):
    return db.query(GroupProduct).filter_by(id = id).first()

def get_groups_products(db: Session, filters: Dict={}):
    query = db.query(GroupProduct)
    if 'product_id' in filters:
        query = query.filter_by(product_id = filters['product_id'])
    if 'tag_id' in filters:
        query = query.filter_by(tag_id = filters['tag_id'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(GroupProduct.created_at))