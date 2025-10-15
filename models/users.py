from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship
import random


class User(Base):

    __tablename__ = "users"
     
    id = Column(BigInteger, primary_key=True, index=True)
    country_id = Column(BigInteger, ForeignKey('countries.id'))
    merchant_id = Column(BigInteger, ForeignKey('merchants.id'))
    username = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    password = Column(String, nullable=True)
    pin = Column(String, nullable=True)
    device_token = Column(String, nullable=True)
    external_provider = Column(String, nullable=True)
    external_reference = Column(String, nullable=True)
    user_type = Column(Integer, default=0)
    role = Column(Integer, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    country = relationship("Country", back_populates='users')
    owned_merchant = relationship('Merchant', back_populates='user', uselist=False, foreign_keys="Merchant.user_id")
    merchant = relationship('Merchant', back_populates='users', foreign_keys=[merchant_id])
    profile = relationship('Profile', back_populates='user', uselist=False)
    orders = relationship('Order', back_populates='user', foreign_keys='Order.user_id')
    favorites = relationship('Favorite', back_populates='user', foreign_keys='Favorite.user_id')
    reviews = relationship('Review', back_populates='user', foreign_keys='Review.user_id')


def create_user(db: Session, country_id: int = 0, merchant_id: int = 0, username: str = None, email: str = None, phone_number: str = None, password: str = None, pin: str = None, device_token: str = None, external_provider: str = None, external_reference: str = None, user_type: int = 0, role: int = 0, status: int = 0, commit: bool=False):
    user = User(country_id=country_id, merchant_id=merchant_id, username=username, email=email, phone_number=phone_number, password=password, pin=pin, device_token=device_token, external_provider=external_provider, external_reference=external_reference, user_type=user_type, role=role, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(user)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(user)
    return user

def update_user(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(User).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_user(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(User).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_user(db: Session, id: int=0, commit: bool=False):
    db.query(User).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_user_by_id(db: Session, id: int=0):
    return db.query(User).filter_by(id = id).first()

def get_main_single_user_by_id(db: Session, id: int=0):
    return db.query(User).options(joinedload(User.merchant), joinedload(User.country), joinedload(User.profile)).filter_by(id = id).first()

def get_single_user_by_email(db: Session, email: str = None):
    return db.query(User).filter_by(email = email).first()

def get_single_user_by_email_and_user_type(db: Session, email: str = None, user_type: int = 0):
    return db.query(User).filter(and_(User.email == email, User.user_type == user_type)).first()

def get_single_user_by_phone_number(db: Session, phone_number: str = None):
    return db.query(User).filter_by(phone_number = phone_number).first()

def get_single_user_by_phone_number_and_user_type(db: Session, phone_number: str = None, user_type: int = 0):
    return db.query(User).filter(and_(User.phone_number == phone_number, User.user_type == user_type)).first()

def get_single_user_by_username(db: Session, username: str = None):
    return db.query(User).filter_by(username = username).first()

def get_single_user_by_username_user_type(db: Session, username: str = None, user_type: int = 0):
    return db.query(User).filter(and_(User.username == username, User.user_type == user_type)).first()

def get_single_user_by_any_main_details(db: Session, email: str = None, phone_number: str = None, username: str = None):
    return db.query(User).filter(or_(User.email == email, User.phone_number == phone_number, User.username == username)).first()

def get_single_searched_user_by_id(db: Session, id: int = 0):
    return db.query(User).filter_by(id = id).options(joinedload(User.profile)).first()

def get_users(db: Session, filters: Dict={}):
    query = db.query(User).options(joinedload(User.merchant), joinedload(User.country), joinedload(User.profile))
    if 'username' in filters:
        query = query.filter(User.username.like("%"+filters['username']+"%"))
    if 'email' in filters:
        query = query.filter(User.email.like("%"+filters['email']+"%"))
    if 'phone_number' in filters:
        query = query.filter(User.phone_number.like("%"+filters['phone_number']+"%"))
    if 'user_type' in filters:
        query = query.filter(User.user_type == filters['user_type'])
    if 'role' in filters:
        query = query.filter(User.role == filters['role'])
    if 'status' in filters:
        query = query.filter(User.status == filters['status'])
    return query.filter(User.deleted_at == None).order_by(desc(User.id))

def get_users_by_country_id(db: Session, country_id: int = 0):
    return db.query(User).filter_by(country_id = country_id).filter(User.deleted_at == None).order_by(desc(User.id))

def get_users_by_merchant_id(db: Session, merchant_id: int = 0):
    return db.query(User).filter_by(merchant_id = merchant_id).filter(User.deleted_at == None).order_by(desc(User.id))

def get_users_by_user_type(db: Session, user_type: int = 0):
    return db.query(User).filter_by(user_type = user_type).filter(User.deleted_at == None).order_by(desc(User.id)).all()

def get_users_by_role(db: Session, role: int = 0):
    return db.query(User).filter_by(role = role).filter(User.deleted_at == None).order_by(desc(User.id))

def get_users_by_user_type_and_role(db: Session, user_type: int = 0, role: int = 0):
    return db.query(User).filter_by(user_type = user_type, role = role).filter(User.deleted_at == None).order_by(desc(User.id))

def search_users(db: Session, filters: Dict={}):
    query = db.query(User).options(joinedload(User.merchant), joinedload(User.country), joinedload(User.profile))
    if 'username' in filters:
        query = query.filter(User.username.like("%"+filters['username']+"%"))
    if 'email' in filters:
        query = query.filter(User.email.like("%"+filters['email']+"%"))
    if 'phone_number' in filters:
        query = query.filter(User.phone_number.like("%"+filters['phone_number']+"%"))
    if 'user_type' in filters:
        query = query.filter(User.user_type == filters['user_type'])
    if 'role' in filters:
        query = query.filter(User.role == filters['role'])
    if 'from_date' in filters and 'to_date' in filters:
        if filters['from_date'] != None and filters['to_date'] != None:
            query = query.filter(and_(User.created_at >= filters['from_date'], User.created_at <= filters['to_date']))
    if 'status' in filters:
        query = query.filter(User.status == filters['status'])
    return query.filter(User.deleted_at == None).order_by(desc(User.id))
    
def search_merchants_and_users(db: Session, merchant_type: int = 0, customer_type: int = 0, filters: Dict={}):
    # query = db.query(User).options(joinedload(User.profile)).filter(or_(User.user_type == merchant_type, User.user_type == customer_type))
    query = db.query(User).options(joinedload(User.profile)).filter(User.user_type == 0)
    if 'ids' in filters:
        query = query.filter(User.id.in_(filters['ids']))
    if 'username' in filters:
        query = query.filter(User.username.like("%"+filters['username']+"%"))
    if 'email' in filters:
        query = query.filter(User.email.like("%"+filters['email']+"%"))
    if 'phone_number' in filters:
        query = query.filter(User.phone_number.like("%"+filters['phone_number']+"%"))
    if 'query' in filters:
        query = query.join(User.profile).filter(or_(User.username.like("%"+filters['query']+"%"), User.email.like("%"+filters['query']+"%"), User.phone_number.like("%"+filters['query']+"%"), Profile.first_name.like("%"+filters['query']+"%"), Profile.last_name.like("%"+filters['query']+"%")))
    if 'role' in filters:
        query = query.filter(User.role == filters['role'])
    if 'from_date' in filters and 'to_date' in filters:
        if filters['from_date'] != None and filters['to_date'] != None:
            query = query.filter(and_(User.created_at >= filters['from_date'], User.created_at <= filters['to_date']))
    if 'status' in filters:
        query = query.filter(User.status == filters['status'])
    return query.filter(User.deleted_at == None).order_by(desc(User.id))

def count_users(db: Session, filters: Dict={}):
    query = db.query(User)
    if 'ids' in filters:
        query = query.filter(User.id.in_(filters['ids']))
    if 'username' in filters:
        query = query.filter(User.username.like("%"+filters['username']+"%"))
    if 'email' in filters:
        query = query.filter(User.email.like("%"+filters['email']+"%"))
    if 'phone_number' in filters:
        query = query.filter(User.phone_number.like("%"+filters['phone_number']+"%"))
    if 'query' in filters:
        query = query.join(User.profile).filter(or_(User.username.like("%"+filters['query']+"%"), User.email.like("%"+filters['query']+"%"), User.phone_number.like("%"+filters['query']+"%"), Profile.first_name.like("%"+filters['query']+"%"), Profile.last_name.like("%"+filters['query']+"%")))
    if 'role' in filters:
        query = query.filter(User.role == filters['role'])
    if 'user_type' in filters:
        query = query.filter(User.user_type == filters['user_type'])
    if 'from_date' in filters and 'to_date' in filters:
        if filters['from_date'] != None and filters['to_date'] != None:
            query = query.filter(and_(User.created_at >= filters['from_date'], User.created_at <= filters['to_date']))
    if 'status' in filters:
        query = query.filter(User.status == filters['status'])
    if 'deleted' in filters:
        query = query.filter(User.deleted_at != None)
    else:
        query = query.filter(User.deleted_at == None)
    return query.count()

def count_users_by_user_type(db: Session, user_type: int=0):
    return db.query(User).filter_by(user_type = user_type).filter(User.deleted_at == None).count()

def get_random_user_by_user_type(db: Session, user_type: int=0):
    # count = count_users_by_user_type(db=db, user_type=user_type)
    # print(count)
    # if count > 0:
    #     offset = random.randint(0, count - 1)
    #     return db.query(User).offset(offset).limit(1).first()
    # else:
    #     return None
    # ids = db.query(User.id).filter_by(user_type = user_type).filter(User.deleted_at == None).scalars().all()
    results = db.query(User.id).filter_by(user_type=user_type).filter(User.deleted_at == None).all()
    ids = [row[0] for row in results]
    print(ids)
    if ids:
        random_id = random.choice(ids)
        print(random_id)
        return db.query(User).filter_by(id = random_id).first()
    else:
        return None