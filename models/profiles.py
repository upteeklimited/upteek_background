from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Profile(Base):

    __tablename__ = "profiles"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    provider_id = Column(BigInteger, default=0)
    compliance_provider_id = Column(BigInteger, default=0)
    compliance_external_reference = Column(String, nullable=True)
    external_reference = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    other_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    mothers_maiden_name = Column(String, nullable=True)
    date_of_birth = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    marital_status = Column(String, nullable=True)
    avatar = Column(Text, nullable=True)
    id_document_file = Column(Text, nullable=True)
    id_document_file_back = Column(Text, nullable=True)
    id_document_type = Column(String, nullable=True)
    id_document_value = Column(String, nullable=True)
    selfie = Column(Text, nullable=True)
    bvn = Column(String, nullable=True)
    bvn_first_name = Column(String, nullable=True)
    bvn_other_name = Column(String, nullable=True)
    bvn_last_name = Column(String, nullable=True)
    bvn_phone_number = Column(String, nullable=True)
    bvn_email = Column(String, nullable=True)
    bvn_date_of_birth = Column(String, nullable=True)
    bvn_external_reference = Column(String, nullable=True)
    bvn_status = Column(SmallInteger, nullable=True)
    bvn_meta_data = Column(Text, nullable=True)
    nin = Column(String, nullable=True)
    nin_first_name = Column(String, nullable=True)
    nin_other_name = Column(String, nullable=True)
    nin_last_name = Column(String, nullable=True)
    nin_phone_number = Column(String, nullable=True)
    nin_email = Column(String, nullable=True)
    nin_date_of_birth = Column(String, nullable=True)
    nin_external_reference = Column(String, nullable=True)
    nin_status = Column(SmallInteger, nullable=True)
    nin_meta_data = Column(Text, nullable=True)
    kyc_level = Column(Integer, nullable=True)
    compliance_request_data = Column(Text, nullable=True)
    compliance_response_data = Column(Text, nullable=True)
    compliance_status = Column(SmallInteger, nullable=True)
    meta_data = Column(Text, nullable=True)
    level_one_approved_by = Column(BigInteger, default=0)
    level_one_rejected_by = Column(BigInteger, default=0)
    level_one_approved_at = Column(TIMESTAMP(timezone=True), nullable=True)
    level_one_rejected_at = Column(TIMESTAMP(timezone=True), nullable=True)
    level_two_approved_by = Column(BigInteger, default=0)
    level_two_rejected_by = Column(BigInteger, default=0)
    level_two_approved_at = Column(TIMESTAMP(timezone=True), nullable=True)
    level_two_rejected_at = Column(TIMESTAMP(timezone=True), nullable=True)
    level_three_approved_by = Column(BigInteger, default=0)
    level_three_rejected_by = Column(BigInteger, default=0)
    level_three_approved_at = Column(TIMESTAMP(timezone=True), nullable=True)
    level_three_rejected_at = Column(TIMESTAMP(timezone=True), nullable=True)
    meta_data = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    user = relationship('User', back_populates='profile')


def create_profile(db: Session, user_id: int = 0, provider_id: int = 0, compliance_provider_id: int = 0, compliance_external_reference: str = None, external_reference: str = None, first_name: str = None, other_name: str = None, last_name: str = None, mothers_maiden_name: str = None, date_of_birth: str = None, gender: str = None, bio: str = None, marital_status: str = None, avatar: str = None, id_document_file: str = None, id_document_file_back: str = None, id_document_type: str = None, id_document_value: str = None, selfie: str = None, bvn: str = None, bvn_first_name: str = None, bvn_other_name: str = None, bvn_last_name: str = None, bvn_phone_number: str = None, bvn_email: str = None, bvn_date_of_birth: str = None, bvn_external_reference: str = None, bvn_status: int = 0, bvn_meta_data: str = None, nin: str = None, nin_first_name: str = None, nin_other_name: str = None, nin_last_name: str = None, nin_phone_number: str = None, nin_email: str = None, nin_date_of_birth: str = None, nin_external_reference: str = None, nin_status: int = 0, nin_meta_data: str = None, kyc_level: int = 0, compliance_request_data: str = None, compliance_response_data: str = None, compliance_status: int = 0, level_one_approved_by: int = 0, level_one_rejected_by: int = 0, level_one_approved_at: str = None, level_one_rejected_at: str = None, level_two_approved_by: int = 0, level_two_rejected_by: int = 0, level_two_approved_at: str = None, level_two_rejected_at: str = None, level_three_approved_by: int = 0, level_three_rejected_by: int = 0, level_three_approved_at: str = None, level_three_rejected_at: str = None, meta_data: str = None, status: int = 0, commit: bool=False):
    profile = Profile(user_id=user_id, provider_id=provider_id, compliance_provider_id=compliance_provider_id, compliance_external_reference=compliance_external_reference, external_reference=external_reference, first_name=first_name, other_name=other_name, last_name=last_name, mothers_maiden_name=mothers_maiden_name, date_of_birth=date_of_birth, gender=gender, bio=bio, marital_status=marital_status, avatar=avatar, id_document_file=id_document_file, id_document_file_back=id_document_file_back, id_document_type=id_document_type, id_document_value=id_document_value, selfie=selfie, bvn=bvn, bvn_first_name=bvn_first_name, bvn_other_name=bvn_other_name, bvn_last_name=bvn_last_name, bvn_phone_number=bvn_phone_number, bvn_email=bvn_email, bvn_date_of_birth=bvn_date_of_birth, bvn_external_reference=bvn_external_reference, bvn_status=bvn_status, bvn_meta_data=bvn_meta_data, nin=nin, nin_first_name=nin_first_name, nin_other_name=nin_other_name, nin_last_name=nin_last_name, nin_phone_number=nin_phone_number, nin_email=nin_email, nin_date_of_birth=nin_date_of_birth, nin_external_reference=nin_external_reference, nin_status=nin_status, nin_meta_data=nin_meta_data, kyc_level=kyc_level, compliance_request_data=compliance_request_data, compliance_response_data=compliance_response_data, compliance_status=compliance_status, level_one_approved_by=level_one_approved_by, level_one_rejected_by=level_one_rejected_by, level_one_approved_at=level_one_approved_at, level_one_rejected_at=level_one_rejected_at, level_two_approved_by=level_two_approved_by, level_two_rejected_by=level_two_rejected_by, level_two_approved_at=level_two_approved_at, level_two_rejected_at=level_two_rejected_at, level_three_approved_by=level_three_approved_by, level_three_rejected_by=level_three_rejected_by, level_three_approved_at=level_three_approved_at, level_three_rejected_at=level_three_rejected_at, meta_data=meta_data, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(profile)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(profile)
    return profile

def update_profile(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Profile).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def update_profile_by_user_id(db: Session, user_id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Profile).filter_by(user_id = user_id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_profile(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Profile).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_profile(db: Session, id: int=0, commit: bool=False):
    db.query(Profile).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_profile_by_id(db: Session, id: int=0):
    return db.query(Profile).filter_by(id = id).first()

def get_single_profile_by_user_id(db: Session, user_id: int = 0):
    return db.query(Profile).filter_by(user_id = user_id).first()

def count_profiles(db: Session, filters: Dict={}):
    query = db.query(Profile)
    if 'user_ids' in filters:
        query = query.filter(Profile.id.in_(filters['user_ids']))
    if 'user_id' in filters:
        query = query.filter(Profile.user_id == filters['user_id'])
    if 'compliance_status' in filters:
        query = query.filter(Profile.compliance_status == filters['compliance_status'])
    if 'status' in filters:
        query = query.filter(Profile.user_id == filters['status'])
    return query.count()
