from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class ComplianceUsage(Base):

    __tablename__ = "compliance_usages"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, default=0)
    provider_id = Column(BigInteger, default=0)
    compliance_product = Column(String, nullable=True)
    request_data = Column(Text, nullable=True)
    response_data = Column(Text, nullable=True)
    from_app = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_compliance_usage(db: Session, user_id: int = 0, provider_id: int = 0, compliance_product: str = None, request_data: str = None,  response_data: str = None, from_app: int = 0, status: int = 0, commit: bool=False):
    cu = ComplianceUsage(user_id=user_id, provider_id=provider_id, compliance_product=compliance_product, request_data=request_data, response_data=response_data, from_app=from_app, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(cu)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(cu)
    return cu

def update_complaince_usage(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(ComplianceUsage).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_compliance_usage(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(ComplianceUsage).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_compliance_usage(db: Session, id: int=0, commit: bool=False):
    db.query(ComplianceUsage).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_complaince_usage_by_id(db: Session, id: int=0):
    return db.query(ComplianceUsage).filter_by(id = id).first()

def get_complaince_usages(db: Session, filters: Dict={}):
    query = db.query(ComplianceUsage)
    if 'user_id' in filters:
        query = query.filter_by(user_id = filters['user_id'])
    if 'provider_id' in filters:
        query = query.filter_by(provider_id = filters['provider_id'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.filter(ComplianceUsage.deleted_at == None).order_by(desc(ComplianceUsage.id))

