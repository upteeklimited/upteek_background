from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class ProductCategory(Base):

    __tablename__ = "products_categories"
     
    id = Column(BigInteger, primary_key=True, index=True)
    category_id = Column(BigInteger, ForeignKey('categories.id'))
    product_id = Column(BigInteger, ForeignKey('products.id'))
    meta_data = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_product_category(db: Session, category_id: int = 0, product_id: int = 0, meta_data: str = None, status: int = 0, commit: bool=False):
    product_category = ProductCategory(category_id=category_id, product_id=product_id, meta_data=meta_data, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(product_category)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(product_category)
    return product_category

def update_product_category(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(ProductCategory).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_product_category(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(ProductCategory).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_product_category(db: Session, id: int=0, commit: bool=False):
    db.query(ProductCategory).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_all_products_categories(db: Session, filters: Dict={}):
    query = db.query(ProductCategory)
    if 'category_id' in filters:
        query = query.filter_by(category_id = filters['category_id'])
    if 'product_id' in filters:
        query = query.filter_by(product_id = filters['product_id'])
    return query.order_by(desc(ProductCategory.created_at))

