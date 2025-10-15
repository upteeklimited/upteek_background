from typing import Dict
from sqlalchemy.orm import Session
from database.model import update_profile_by_user_id, update_setting_by_user_id, get_single_user_by_id, update_user
from modules.utils.tools import process_schema_dictionary
from modules.utils.auth import AuthHandler

auth = AuthHandler()


def update_user_profile_details(db: Session, user_id: int=0, values: Dict={}):
    passvalues = process_schema_dictionary(info=values)
    update_profile_by_user_id(db=db, user_id=user_id, values=passvalues)
    return {
        'status': True,
        'message': 'Success'
    }

def update_user_password(db: Session, user_id: int=0, password: str=None, old_password: str=None):
    user = get_single_user_by_id(db=db, id=user_id)
    if user is None:
        return {
            'status': False,
            'message': 'User not found',
        }
    else:
        if auth.verify_password(plain_password=old_password, hashed_password=user.password) == False:
            return {
                'status': False,
                'message': 'Old Password Incorrect'
            }
        else:
            password = auth.get_password_hash(password=password)
            da = {
                'password': password
            }
            update_user(db=db, id=user_id, values=da)
            return {
                'status': True,
                'message': 'Success'
            }

def update_user_settings(db: Session, user_id: int=0, values: Dict={}):
    passvalues = process_schema_dictionary(info=values)
    update_setting_by_user_id(db=db, user_id=user_id, values=passvalues)
    return {
        'status': True,
        'message': 'Success'
    }
