from typing import Dict
from sqlalchemy.orm import Session
from database.model import get_single_financial_product_by_id, get_financial_products
from fastapi_pagination.ext.sqlalchemy import paginate


def retrieve_financial_products(db: Session, filters: Dict={}):
    data = get_financial_products(db=db, filters=filters)
    return paginate(data)

def retrieve_single_financial_product(db: Session, product_id: int=0):
    product = get_single_financial_product_by_id(db=db, id=product_id)
    if product is None:
        return {
            'status': False,
            'message': 'Financial Product not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': product,
        }