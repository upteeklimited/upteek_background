from typing import Dict
from sqlalchemy.orm import Session
from database.model import search_merchants_and_users, get_reviews, get_single_searched_user_by_id, get_single_review_by_id, count_profiles, count_users
from fastapi_pagination.ext.sqlalchemy import paginate as sql_paginate
from fastapi_pagination import paginate
from settings.constants import USER_TYPES

def retrieve_merchants_and_customers(db: Session, filters: Dict = {}):
    data = search_merchants_and_users(db=db, merchant_type=USER_TYPES['merchant']['num'], customer_type=USER_TYPES['customer']['num'], filters=filters)
    return sql_paginate(data)

def retrieve_single_user(db: Session, id: int = 0):
    user = get_single_searched_user_by_id(db=db, id=id)
    if user is None:
        return {
            'status': False,
            'message': 'User not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': user
        }
    
def retrieve_reviews(db: Session, product_id: int=0, merchant_id: int=0, filters: Dict={}):
    if product_id:
        filters['reviewable_id'] = product_id
        filters['reviewable_type'] = "product"
    if merchant_id:
        filters['reviewable_id'] = merchant_id
        filters['reviewable_type'] = "merchant"
    data = get_reviews(db=db, filters=filters)
    return sql_paginate(data)

def retrieve_single_review(db: Session, review_id: int=0):
    review = get_single_review_by_id(db=db, id=review_id)
    if review is None:
        return {
            'status': False,
            'message': 'Review not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': review
        }

def retrieve_customers_stats(db: Session):
    total_registered = count_users(db=db, filters={'user_type': 0})
    total_active = count_users(db=db, filters={'user_type': 0, 'status': 1})
    total_suspended = count_users(db=db, filters={'user_type': 0, 'status': 0})
    total_deactivated = count_users(db=db, filters={'user_type': 0, 'deleted': 0})
    total_compliance_done = count_profiles(db=db, filters={'compliance_status': 1})
    data = {
        "total_registered": total_registered,
        "total_active": total_active,
        "total_suspended": total_suspended,
        "total_deactivated": total_deactivated,
        "total_compliance_done": total_compliance_done,
    }
    return {
        "status": True,
        "message": "Success",
        "data": data,
    }
