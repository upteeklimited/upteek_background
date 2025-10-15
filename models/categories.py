from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Category(Base):

    __tablename__ = "categories"
     
    id = Column(BigInteger, primary_key=True, index=True)
    merchant_id = Column(BigInteger, default=0)
    category_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    slug = Column(String, nullable=True)
    icon = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    authorized_by = Column(BigInteger, default=0)
    authorized_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    products = relationship("Product", secondary="products_categories", back_populates="categories")

def create_category(db: Session, merchant_id: int = 0, category_id: int = 0, name: str = None, description: str = None, slug: str = None, icon: str = None, status: int = 0, created_by: int = 0, authorized_by: int = 0, authorized_at: str = None, commit: bool=False):
    category = Category(merchant_id=merchant_id, category_id=category_id, name=name, description=description, slug=slug, icon=icon, status=status, created_by=created_by, authorized_by=authorized_by, authorized_at=authorized_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(category)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(category)
    return category

def update_category(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Category).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_category(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Category).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_category(db: Session, id: int=0, commit: bool=False):
    db.query(Category).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_category_by_id(db: Session, id: int=0):
    return db.query(Category).filter_by(id = id).first()

def get_single_category_by_slug(db: Session, slug: str=None):
    return db.query(Category).filter_by(slug = slug).first()

def get_categories(db: Session, filters: Dict={}):
    query = db.query(Category)
    if 'merchant_id' in filters:
        query = query.filter_by(merchant_id = filters['merchant_id'])
    if 'category_id' in filters:
        query = query.filter_by(category_id = filters['category_id'])
    if 'name' in filters:
        query = query.filter(Category.name.like('%' + filters['name'] + '%'))
    if 'slug' in filters:
        query = query.filter(Category.slug.like('%' + filters['slug'] + '%'))
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    if 'created_by' in filters:
        query = query.filter_by(created_by = filters['created_by'])
    if 'authorized_by' in filters:
        query = query.filter_by(authorized_by = filters['authorized_by'])
        query = query.filter_by(deleted_at = filters['deleted_at'])
    return query.order_by(desc(Category.created_at))

