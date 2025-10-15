from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from database.custom_types import JSONText
from sqlalchemy.orm import relationship


class ProductVariant(Base):

    __tablename__ = "product_variants"
     
    id = Column(BigInteger, primary_key=True, index=True)
    product_id = Column(BigInteger, ForeignKey('products.id'))
    attributes = Column(Text, nullable=True)
    amount = Column(Float, default=0)
    files_meta_data = Column(JSONText)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    product = relationship("Product", back_populates="variants")

def create_product_variant(db: Session, product_id: int = 0, attributes: str = None, amount: float = 0, files_meta_data: str = None, status: int = 0, commit: bool=False):
    pv = ProductVariant(product_id=product_id, attributes=attributes, amount=amount, files_meta_data=files_meta_data, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(pv)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(pv)
    return pv

def update_product_variant(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(ProductVariant).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_product_variant(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(ProductVariant).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_product_variant(db: Session, id: int=0, commit: bool=False):
    db.query(ProductVariant).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_product_variant_by_id(db: Session, id: int=0):
    return db.query(ProductVariant).filter_by(id = id).first()

def get_product_variants(db: Session, filters: Dict={}):
    query = db.query(ProductVariant)
    if 'product_id' in filters:
        query = query.filter_by(product_id = filters['product_id'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(ProductVariant.created_at))