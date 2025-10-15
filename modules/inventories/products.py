from typing import Dict, List
from sqlalchemy.orm import Session
from database.model import get_products, get_single_product_by_id, get_single_product_by_slug, get_reviews
from fastapi_pagination.ext.sqlalchemy import paginate
import json

def retrieve_products(db: Session, filters: Dict={}):
    data = get_products(db=db, filters=filters)
    return paginate(data)

def retrieve_single_product(db: Session, id: int=0):
    product = get_single_product_by_id(db=db, id=id)
    if product is None:
        return {
            'status': False,
            'message': 'Product not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': product
        }
    
def retrieve_single_product_by_slug(db: Session, slug: str=None):
    product = get_single_product_by_slug(db=db, slug=slug)
    if product is None:
        return {
            'status': False,
            'message': 'Product not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': product
        }

def retrieve_product_reviews(db: Session, product_id: int=0, filters: Dict={}):
    filters['reviewable_id'] = product_id
    filters['reviewable_type'] = "product"
    data = get_reviews(db=db, filters=filters)
    return paginate(data)