from typing import Dict
from sqlalchemy.orm import Session
from database.model import create_merchant_industry, update_merchant_industry, delete_merchant_industry, get_merchant_industries, get_single_merchant_industry_by_id, create_merchant_category, update_merchant_category, delete_merchant_category, get_merchant_categories, get_single_merchant_category_by_id
from modules.utils.tools import process_schema_dictionary
from fastapi_pagination.ext.sqlalchemy import paginate

def create_new_merchant_industry(db: Session, name: str = None, description: str = None):
    industry = create_merchant_industry(db=db, name=name, description=description)
    return {
        'status': True,
        'message': 'Success',
        'data': industry,
    }

def update_existing_merchant_industry(db: Session, industry_id: int=0,values: Dict={}):
    values = process_schema_dictionary(info=values)
    update_merchant_industry(db=db, id=industry_id, values=values)
    return {
        'status': True,
        'message': 'Success'
    }

def delete_existing_merchant_industry(db: Session, industry_id: int=0):
    delete_merchant_industry(db=db, id=industry_id)
    return {
        'status': True,
        'message': 'Success'
    }

def retrieve_merchant_industries(db: Session):
    industries = get_merchant_industries(db=db)
    return paginate(industries)

def retrieve_single_merchant_industry(db: Session, industry_id: int=0):
    industry = get_single_merchant_industry_by_id(db=db, id=industry_id)
    if industry is None:
        return {
            'status': False,
            'message': 'Merchant Industry not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': industry
        }

def create_new_merchant_category(db: Session, industry_id: int=0, name: str = None, description: str = None):
    category = create_merchant_category(db=db, industry_id=industry_id, name=name, description=description)
    return {
        'status': True,
        'message': 'Success',
        'data': category,
    }

def update_existing_merchant_category(db: Session, category_id: int=0, values: Dict={}):
    values = process_schema_dictionary(info=values)
    update_merchant_category(db=db, id=category_id, values=values)
    return {
        'status': True,
        'message': 'Success'
    }

def delete_existing_merchant_category(db: Session, category_id: int=0):
    delete_merchant_category(db=db, id=category_id)
    return {
        'status': True,
        'message': 'Success'
    }

def retrieve_merchant_categories(db: Session, filters: Dict={}):
    categories = get_merchant_categories(db=db, filters=filters)
    return paginate(categories)

def retrieve_single_merchant_category(db: Session, category_id: int=0):
    category = get_single_merchant_category_by_id(db=db, id=category_id)
    if category is None:
        return {
            'status': False,
            'message': 'Merchant Category not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': category
        }