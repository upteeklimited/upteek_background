from typing import Dict
from sqlalchemy.orm import Session
from database.model import get_single_general_ledger_account_type_by_id, get_single_general_ledger_account_type_by_account_code, get_general_ledger_account_types
from fastapi_pagination.ext.sqlalchemy import paginate

def retrieve_gl_types(db: Session, filters: Dict={}):
    data = get_general_ledger_account_types(db=db, filters=filters)
    return paginate(data)

def retrieve_single_gl_type(db: Session, gl_type_id: int=0):
    gl_type = get_single_general_ledger_account_type_by_id(db=db, id=gl_type_id)
    if gl_type is None:
        return {
            'status': False,
            'message': 'General Ledger Type not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': gl_type,
        }
    
def retrieve_single_gl_type_by_code(db: Session, code: str=None):
    gl_type = get_single_general_ledger_account_type_by_account_code(db=db, account_code=code)
    if gl_type is None:
        return {
            'status': False,
            'message': 'General Ledger Type not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': gl_type,
        }