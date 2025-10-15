from typing import Dict
from sqlalchemy.orm import Session
from database.model import get_transaction_types, get_single_transaction_type_by_id, get_single_transaction_type_by_code
from fastapi_pagination.ext.sqlalchemy import paginate

def retrive_transaction_type(db: Session, filters: Dict={}):
    data = get_transaction_types(db=db, filters=filters)
    return paginate(data)

def retrieve_single_transaction_type(db: Session, type_id: int=0):
    trans_type = get_single_transaction_type_by_id(db=db, id=type_id)
    if trans_type is None:
        return {
            'status': False,
            'message': 'Transaction Type not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': trans_type,
        }
    
def retrieve_single_transaction_type_by_code(db: Session, code: str=None):
    trans_type = get_single_transaction_type_by_code(db=db, code=code)
    if trans_type is None:
        return {
            'status': False,
            'message': 'Transaction Type not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': trans_type,
        }