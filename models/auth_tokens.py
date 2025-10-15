from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class AuthToken(Base):

    __tablename__ = "auth_tokens"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, default=0)
    token = Column(String, nullable=True)
    device_token = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    expired_at = Column(TIMESTAMP(timezone=True), nullable=True)
    last_ping_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_auth_token(db: Session, user_id: int = 0, token: str = None, device_token: str = None, status: int = 0, expired_at: str = None, last_ping_at: str = None, commit: bool=False):
    auth_token = AuthToken(user_id=user_id, token=token, device_token=device_token, status=status, expired_at=expired_at, last_ping_at=last_ping_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(auth_token)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(auth_token)
    return auth_token

def update_auth_token(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(AuthToken).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def update_user_auth_token(db: Session, user_id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(AuthToken).filter_by(user_id = user_id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_auth_token(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(AuthToken).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_auth_token(db: Session, id: int=0, commit: bool=False):
    db.query(AuthToken).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_auth_token_by_id(db: Session, id: int=0):
    return db.query(AuthToken).filter_by(id = id).first()

def get_auth_tokens(db: Session):
    return db.query(AuthToken).filter(AuthToken.deleted_at == None).order_by(desc(AuthToken.id))

def get_auth_tokens_by_user_id(db: Session, user_id: int = 0):
    return db.query(AuthToken).filter_by(user_device_id = user_id).filter(AuthToken.deleted_at == None).order_by(desc(AuthToken.id))

def get_latest_user_auth_token(db: Session, user_id: int = 0):
    return db.query(AuthToken).filter_by(user_id = user_id).filter(AuthToken.deleted_at == None).order_by(desc(AuthToken.id)).first()
