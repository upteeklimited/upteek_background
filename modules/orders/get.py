from typing import Dict, List, Any
import dateparser
from sqlalchemy.orm import Session
from database.model import get_orders, get_single_order_by_id, count_orders
from fastapi_pagination.ext.sqlalchemy import paginate

def retrieve_orders(db: Session, filters: Dict={}):
    if 'from_date' in filters:
        if filters['from_date'] is not None:
            filters['from_date'] = dateparser.parse(filters['from_date'])
    if 'to_date' in filters:
        if filters['to_date'] is not None:
            filters['to_date'] = dateparser.parse(filters['to_date'])
    data = get_orders(db=db, filters=filters)
    return paginate(data)

def retrieve_single_order(db: Session, id: int=0):
    order = get_single_order_by_id(db=db, id=id)
    if order is None:
        return {
            'status': False,
            'message': 'Order not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': order
        }

def retrieve_order_stats(db: Session):
    total_order = count_orders(db=db)
    pending_order = count_orders(db=db, filters={'status': 0})
    completed_order = count_orders(db=db, filters={'status': 1})
    failed_order = count_orders(db=db, filters={'status': 3})
    data = {
        "total_order": total_order,
        "pending_order": pending_order,
        "completed_order": completed_order,
        "failed_order": failed_order,
    }
    return {
        "status": True,
        "message": "Success",
        "data": data
    }