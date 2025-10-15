from typing import Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from database.custom_types import JSONText
from sqlalchemy.orm import relationship, foreign
from models.favorites import Favorite
from models.reviews import Review
from models.users import User
import random


class Product(Base):

    __tablename__ = "products"
     
    id = Column(BigInteger, primary_key=True, index=True)
    merchant_id = Column(BigInteger, ForeignKey('merchants.id'))
    category_id = Column(BigInteger, ForeignKey('categories.id'))
    currency_id = Column(BigInteger, ForeignKey('currencies.id'))
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    slug = Column(String, nullable=True)
    product_type = Column(Integer, default=0)
    service_pricing = Column(Integer, default=0)
    units = Column(Integer, default=0)
    weight = Column(Float, default=0)
    cost_price = Column(Float, default=0)
    price = Column(Float, default=0)
    minimum_price = Column(Float, default=0)
    maximum_price = Column(Float, default=0)
    discount_price = Column(Float, default=0)
    discount = Column(Float, default=0)
    discount_type = Column(Integer, default=0)
    special_note = Column(Text, nullable=True)
    unit_low_level = Column(Integer, default=0)
    files_meta_data = Column(JSONText)
    service_delivery_mode = Column(Integer, default=0)
    service_is_time_sensitive = Column(Integer, default=0)
    service_invoice_validity_hours = Column(String, nullable=True)
    service_addon_extra_charge_meta_data = Column(JSONText)
    service_available_days_data = Column(JSONText)
    service_available_time_data = Column(JSONText)
    service_delivery_mode_data = Column(JSONText)
    service_required_details_data = Column(JSONText)
    meta_data = Column(Text, nullable=True)
    notify_if_available = Column(SmallInteger, default=0)
    condition_status = Column(Integer, default=0)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    authorized_by = Column(BigInteger, default=0)
    authorized_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    merchant = relationship("Merchant")
    category = relationship("Category")
    categories = relationship("Category", secondary="products_categories", back_populates="products")
    currency = relationship("Currency")
    tags = relationship("Tag", secondary="tags_products", back_populates="products")
    groups = relationship("Group", secondary="groups_products", back_populates="products")
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
    order_products = relationship("OrderProduct", back_populates="product")
    cart_products = relationship("CartProduct", back_populates="product")
    payment_links = relationship("PaymentLink", back_populates="product")
    paymentlink_products = relationship("PaymentLinkProduct", back_populates="product")
    reviews = relationship(
        "Review",
        primaryjoin=lambda: and_(
            foreign(Review.reviewable_id) == Product.id,
            Review.reviewable_type == 'product'
        ),
        viewonly=True
    )
    favorable = relationship(
        "Favorite",
        primaryjoin=lambda: and_(
            foreign(Favorite.favoriteable_id) == Product.id,
            Favorite.favoriteable_type == 'product'
        ),
        viewonly=True
    )

def create_product(db: Session, merchant_id: int = 0, category_id: int = 0, currency_id: int = 0, name: str = None, description: str = None, slug: str = None, product_type: int = 0, service_pricing: int = 0, units: int = 0, weight: float = 0, cost_price: float = 0, price: float = 0, minimum_price: float = 0, maximum_price: float = 0, discount_price: float = 0, discount: float = 0, discount_type: int = 0, special_note: str = None, unit_low_level: int = 0, files_meta_data: Any = None, service_delivery_mode: int = 0, service_is_time_sensitive: int = 0, service_invoice_validity_hours: str = None, service_addon_extra_charge_meta_data: Any = None, service_available_days_data: Any = None, service_available_time_data: Any = None, service_delivery_mode_data: Any = None, service_required_details_data: Any = None, meta_data: str = None, notify_if_available: int = 0, condition_status: int = 0, status: int = 0, created_by: int = 0, authorized_by: int = 0, authorized_at: str = None, commit: bool=False):
    product = Product(merchant_id=merchant_id, category_id=category_id, currency_id=currency_id, name=name, description=description, slug=slug, product_type=product_type, service_pricing=service_pricing, units=units, weight=weight, cost_price=cost_price, price=price, minimum_price=minimum_price, maximum_price=maximum_price, discount_price=discount_price, discount=discount, discount_type=discount_type, special_note=special_note, unit_low_level=unit_low_level, files_meta_data=files_meta_data, service_delivery_mode=service_delivery_mode, service_is_time_sensitive=service_is_time_sensitive, service_invoice_validity_hours=service_invoice_validity_hours, service_addon_extra_charge_meta_data=service_addon_extra_charge_meta_data, service_available_days_data=service_available_days_data, service_available_time_data=service_available_time_data, service_delivery_mode_data=service_delivery_mode_data, service_required_details_data=service_required_details_data, meta_data=meta_data, notify_if_available=notify_if_available, condition_status=condition_status, status=status, created_by=created_by, authorized_by=authorized_by, authorized_at=authorized_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(product)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(product)
    return product

def update_product(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Product).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_product(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Product).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_product(db: Session, id: int=0, commit: bool=False):
    db.query(Product).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_product_by_id(db: Session, id: int=0):
    return db.query(Product).options(joinedload(Product.merchant), joinedload(Product.category), joinedload(Product.categories), joinedload(Product.currency), joinedload(Product.tags)).filter_by(id = id).first()

def get_single_product_by_slug(db: Session, slug: str=None):
    return db.query(Product).options(joinedload(Product.merchant), joinedload(Product.category), joinedload(Product.categories), joinedload(Product.currency), joinedload(Product.tags)).filter_by(slug = slug).first()

def get_products_by_merchant_id(db: Session, merchant_id: int = 0):
    return db.query(Product).filter_by(merchant_id = merchant_id).all()

def get_products(db: Session, filters: Dict={}):
    query = db.query(Product).options(joinedload(Product.merchant), joinedload(Product.category), joinedload(Product.categories), joinedload(Product.currency), joinedload(Product.tags))
    if 'merchant_id' in filters:
        query = query.filter_by(merchant_id = filters['merchant_id'])
    if 'category_id' in filters:
        query = query.filter_by(category_id = filters['category_id'])
    if 'currency_id' in filters:
        query = query.filter_by(currency_id = filters['currency_id'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    if 'name' in filters:
        query = query.filter(Product.name.like("%" + filters['name'] + "%"))
    if 'slug' in filters:
        query = query.filter(Product.slug.like('%' + filters['slug'] + '%'))
    return query.order_by(desc(Product.created_at))

def count_products(db: Session):
    return db.query(Product).count()

def count_products_by_merchant_id(db: Session, merchant_id: int = 0):
    print(merchant_id)
    return db.query(Product).filter_by(merchant_id = merchant_id).count()

def get_random_merchant_product(db: Session, merchant_id: int=0):
    results = db.query(Product.id).filter_by(merchant_id = merchant_id).all()
    ids = [row[0] for row in results]
    print(ids)
    if ids:
        random_id = random.choice(ids)
        print(random_id)
        return db.query(Product).filter_by(id = random_id).first()
    else:
        return None