from typing import Dict
from sqlalchemy.orm import Session
from database.model import get_account_types, get_single_account_type_by_id, get_single_account_type_by_account_code, get_accounts, get_single_account_by_id, get_single_account_by_account_number, get_virtual_accounts, get_single_virtual_account_by_id, get_single_financial_product_by_id, get_last_account, create_account
from modules.utils.acct import generate_internal_account_number
from fastapi_pagination.ext.sqlalchemy import paginate

def retrieve_account_types(db: Session, filters: Dict={}):
    data = get_account_types(db=db, filters=filters)
    return paginate(data)

def retrieve_single_account_type(db: Session, account_type_id: int=0):
    account_type = get_single_account_type_by_id(db=db, id=account_type_id)
    if account_type is None:
        return {
            'status': False,
            'message': 'Account Type not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': account_type,
        }
    
def retrieve_single_account_type_by_code(db: Session, account_code: str=None):
    account_type = get_single_account_type_by_account_code(db=db, account_code=account_code)
    if account_type is None:
        return {
            'status': False,
            'message': 'Account Type not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': account_type,
        }

def retrieve_accounts(db: Session, filters: Dict={}):
    data = get_accounts(db=db, filters=filters)
    return paginate(data)

def retrieve_single_account(db: Session, account_id: int=0):
    account = get_single_account_by_id(db=db, id=account_id)
    if account is None:
        return {
            'status': False,
            'message': 'Account not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': account,
        }

def retrieve_single_account_by_number(db: Session, account_number: str=None):
    account = get_single_account_by_account_number(db=db, account_number=account_number)
    if account is None:
        return {
            'status': False,
            'message': 'Account not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': account,
        }
    
def retrieve_virtual_accounts(db: Session, filters: Dict={}):
    data = get_virtual_accounts(db=db, filters=filters)
    return paginate(data)

def retrive_single_virtual_account(db: Session, virtual_account_id: int=0):
    va = get_single_account_by_id(db=db, id=virtual_account_id)
    if va is None:
        return {
            'status': False,
            'message': 'Virtual Account not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': va,
        }
