from typing import Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from database.custom_types import JSONText
from sqlalchemy.orm import relationship


class WalletConfiguration(Base):

    __tablename__ = "wallet_configurations"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, default=0)
    merchant_id = Column(BigInteger, default=0)
    primary_account_id = Column(BigInteger, default=0)
    collection_account_id = Column(BigInteger, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_wallet_configuration(db: Session, user_id: int = 0, merchant_id: int = 0, primary_account_id: int = 0, collection_account_id: int = 0, status: int = 0, commit: bool=False):
    wallet_config = WalletConfiguration(user_id=user_id, merchant_id=merchant_id, primary_account_id=primary_account_id, collection_account_id=collection_account_id, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(wallet_config)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(wallet_config)
    return wallet_config

def update_wallet_configuration(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(WalletConfiguration).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_wallet_configuration(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(WalletConfiguration).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_wallet_configuration(db: Session, id: int=0, commit: bool=False):
    db.query(WalletConfiguration).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_wallet_configuration_by_id(db: Session, id: int=0):
    return db.query(WalletConfiguration).filter_by(id = id).first()

def get_single_wallet_configuration_by_user_id(db: Session, user_id: int=0):
    return db.query(WalletConfiguration).filter_by(user_id = user_id).first()

def get_single_wallet_configuration_by_merchant_id(db: Session, merchant_id: int=0):
    return db.query(WalletConfiguration).filter_by(merchant_id = merchant_id).first()
