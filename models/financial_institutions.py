from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class FinancialInstitution(Base):

    __tablename__ = "financial_institutions"
     
    id = Column(BigInteger, primary_key=True, index=True)
    provider_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    code = Column(String, nullable=True)
    nibss_code = Column(String, nullable=True)
    extra_code = Column(String, nullable=True)
    category = Column(String, nullable=True)
    icon = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_financial_institution(db: Session, provider_id: int = 0, name: str = None, code: str = None, nibss_code: str = None, extra_code: str = None, category: str = None, icon: str = None, status: int = 0, commit: bool=False):
    financial_institution = FinancialInstitution(provider_id=provider_id, name=name, code=code, nibss_code=nibss_code, extra_code=extra_code, category=category, icon=icon, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(financial_institution)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(financial_institution)
    return financial_institution

def update_financial_institution(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(FinancialInstitution).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_financial_institution(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(FinancialInstitution).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_financial_institution(db: Session, id: int=0, commit: bool=False):
    db.query(FinancialInstitution).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_financial_institution_by_id(db: Session, id: int=0):
    return db.query(FinancialInstitution).filter_by(id = id).first()

def get_financial_institutions(db: Session, filters: Dict={}):
    query = db.query(FinancialInstitution)
    if 'name' in filters:
        query = query.filter(FinancialInstitution.name.like("%"+filters['name']+"%"))
    if 'code' in filters:
        query = query.filter(FinancialInstitution.code.like("%"+filters['code']+"%"))
    if 'category' in filters:
        query = query.filter(FinancialInstitution.category.like("%"+filters['category']+"%"))
    if 'status' in filters:
        query = query.filter(FinancialInstitution.status == filters['status'])
    return query.order_by(desc(FinancialInstitution.created_at))