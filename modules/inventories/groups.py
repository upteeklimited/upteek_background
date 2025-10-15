from typing import Dict
from sqlalchemy.orm import Session
from database.model import get_groups, get_single_group_by_id
from fastapi_pagination.ext.sqlalchemy import paginate

def retrieve_groups(db: Session, filters: Dict={}):
    data = get_groups(db=db, filters=filters)
    return paginate(data)

def retrieve_single_group(db: Session, id: int=0):
    group = get_single_group_by_id(db=db, id=id)
    if group is None:
        return {
            'status': False,
            'message': 'Group not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': group
        }