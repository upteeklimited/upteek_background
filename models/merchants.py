from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship
from models.merchants_users import Merchant_User
from models.users import User
from models.accounts import Account


class Merchant(Base):

    __tablename__ = "merchants"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(BigInteger, ForeignKey('merchant_categories.id'))
    currency_id = Column(BigInteger, ForeignKey('currencies.id'))
    compliance_provider_id = Column(BigInteger, default=0)
    compliance_external_reference = Column(String, nullable=True)
    name = Column(String, nullable=True)
    trading_name = Column(String, nullable=True)
    slug = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    email = Column(String, nullable=True)
    phone_number_one = Column(String, nullable=True)
    phone_number_two = Column(String, nullable=True)
    opening_hours = Column(String, nullable=True)
    closing_hours = Column(String, nullable=True)
    logo = Column(Text, nullable=True)
    banner = Column(Text, nullable=True)
    thumbnail = Column(Text, nullable=True)
    certificate = Column(Text, nullable=True)
    memorandum = Column(Text, nullable=True)
    utility_bill = Column(Text, nullable=True)
    building = Column(Text, nullable=True)
    tax_id = Column(Text, nullable=True)
    registration_type = Column(Text, nullable=True)
    registration_number = Column(Text, nullable=True)
    compliance_request_data = Column(Text, nullable=True)
    compliance_response_data = Column(Text, nullable=True)
    compliance_status = Column(SmallInteger, default=0)
    compliance_approved_by = Column(BigInteger, default=0)
    compliance_approved_at = Column(TIMESTAMP(timezone=True), nullable=True)
    compliance_rejected_by = Column(BigInteger, default=0)
    compliance_rejected_at = Column(TIMESTAMP(timezone=True), nullable=True)
    accept_vat = Column(SmallInteger, default=0)
    accept_wht = Column(SmallInteger, default=0)
    meta_data = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    user = relationship('User', back_populates='owned_merchant', foreign_keys=[user_id])
    users = relationship('User', back_populates='merchant', foreign_keys='User.merchant_id')
    account = relationship('Account', primaryjoin="and_(Merchant.id==Account.merchant_id, Account.is_primary==1)", back_populates='merchant', uselist=False)
    category = relationship('MerchantCategory')
    currency = relationship('Currency')
    orders = relationship('Order', back_populates='merchant', foreign_keys='Order.merchant_id')
    payment_links = relationship('PaymentLink', back_populates='merchant', foreign_keys='PaymentLink.merchant_id')
    merchant_users = relationship("Merchant_User", back_populates="merchant")


def create_merchant(db: Session, user_id: int = 0, category_id: int = 0, currency_id: int = 0, compliance_provider_id: int = 0, compliance_external_reference: str = None, name: str = None, trading_name: str = None, slug: str = None, description: str = None, email: str = None, phone_number_one: str = None, phone_number_two: str = None, opening_hours: str = None, closing_hours: str = None, logo: str = None, banner: str = None, thumbnail: str = None, certificate: str = None, memorandum: str = None, utility_bill: str = None, building: str = None, tax_id: str = None, registration_type: str = None, registration_number: str = None, compliance_request_data: str = None, compliance_response_data: str = None, compliance_status: int = 0, compliance_approved_by: int = 0, compliance_approved_at: str = None, compliance_rejected_by: int = 0, compliance_rejected_at: str = None, accept_vat: int = 0, accept_wht: int = 0, meta_data: str = None, status: int = 0, commit: bool=False):
    merchant = Merchant(user_id=user_id, category_id=category_id, currency_id=currency_id, compliance_provider_id=compliance_provider_id, compliance_external_reference=compliance_external_reference, name=name, trading_name=trading_name, slug=slug, description=description, email=email, phone_number_one=phone_number_one, phone_number_two=phone_number_two, opening_hours=opening_hours, closing_hours=closing_hours, logo=logo, banner=banner, thumbnail=thumbnail, certificate=certificate, memorandum=memorandum, utility_bill=utility_bill, building=building, tax_id=tax_id, registration_type=registration_type, registration_number=registration_number, compliance_request_data=compliance_request_data, compliance_response_data=compliance_response_data, compliance_status=compliance_status, compliance_approved_by=compliance_approved_by, compliance_approved_at=compliance_approved_at,compliance_rejected_by=compliance_rejected_by, compliance_rejected_at=compliance_rejected_at, accept_vat=accept_vat, accept_wht=accept_wht, meta_data=meta_data, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(merchant)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(merchant)
    return merchant

def update_merchant(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Merchant).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_merchant(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Merchant).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_merchant(db: Session, id: int=0, commit: bool=False):
    db.query(Merchant).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_merchant_by_id(db: Session, id: int=0):
    return db.query(Merchant).filter_by(id = id).first()

def get_main_single_merchant_by_id(db: Session, id: int=0):
    return db.query(Merchant).options(joinedload(Merchant.user), joinedload(Merchant.category), joinedload(Merchant.currency)).filter_by(id = id).first()

def get_single_merchant_by_user_id(db: Session, user_id: int=0):
    return db.query(Merchant).filter_by(user_id = user_id).first()

def get_merchants(db: Session, filters: Dict={}):
    query = db.query(Merchant).options(joinedload(Merchant.category), joinedload(Merchant.currency), joinedload(Merchant.merchant_users).joinedload(Merchant_User.user).joinedload(User.profile), joinedload(Merchant.account).joinedload(Account.virtual_account))
    if 'user_id' in filters:
        query = query.filter(Merchant.user_id == filters['user_id'])
    if 'category_id' in filters:
        query = query.filter(Merchant.category_id == filters['category_id'])
    if 'currency_id' in filters:
        query = query.filter(Merchant.currency_id == filters['currency_id'])
    if 'name' in filters:
        query = query.filter(Merchant.name.ilike(f"%{filters['name']}%"))
    if 'slug' in filters:
        query = query.filter(Merchant.slug.ilike(f"%{filters['slug']}%"))
    if 'compliance_status' in filters:
        query = query.filter(Merchant.compliance_status == filters['compliance_status'])
    if 'status' in filters:
        query = query.filter(Merchant.status == filters['status'])
    if 'user_ids' in filters:
        query = query.join(Merchant_User, Merchant_User.merchant_id == Merchant.id).filter(Merchant_User.id.in_(filters['user_ids']))
    if 'from_date' in filters and 'to_date' in filters:
        if filters['from_date'] != None and filters['to_date'] != None:
            query = query.filter(and_(Merchant.created_at >= filters['from_date'], Merchant.created_at <= filters['to_date']))
    if 'deleted' in filters:
        query = query.filter(Merchant.deleted_at != None)
    else:
        query = query.filter(Merchant.deleted_at == None)
    return query.filter(Merchant.deleted_at == None).order_by(desc(Merchant.id))

def get_merchants_by_category_id(db: Session, category_id: int=0):
    return db.query(Merchant).filter_by(category_id = category_id).filter(Merchant.deleted_at == None).order_by(desc(Merchant.id))

def count_merchants(db: Session, filters: Dict={}):
    query = db.query(Merchant)
    if 'user_id' in filters:
        query = query.filter(Merchant.user_id == filters['user_id'])
    if 'category_id' in filters:
        query = query.filter(Merchant.category_id == filters['category_id'])
    if 'currency_id' in filters:
        query = query.filter(Merchant.currency_id == filters['currency_id'])
    if 'name' in filters:
        query = query.filter(Merchant.name.ilike(f"%{filters['name']}%"))
    if 'slug' in filters:
        query = query.filter(Merchant.slug.ilike(f"%{filters['slug']}%"))
    if 'compliance_status' in filters:
        query = query.filter(Merchant.compliance_status == filters['compliance_status'])
    if 'from_date' in filters and 'to_date' in filters:
        if filters['from_date'] != None and filters['to_date'] != None:
            query = query.filter(and_(Merchant.created_at >= filters['from_date'], Merchant.created_at <= filters['to_date']))
    if 'status' in filters:
        query = query.filter(Merchant.status == filters['status'])
    if 'deleted' in filters:
        query = query.filter(Merchant.deleted_at != None)
    else:
        query = query.filter(Merchant.deleted_at == None)
    return query.count()