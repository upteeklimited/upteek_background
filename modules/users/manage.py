from typing import Dict
from sqlalchemy.orm import Session
from database.model import registration_unique_field_check, create_user_with_relevant_rows, update_user, delete_user, get_main_single_user_by_id, get_users, search_users, get_single_country_by_code, get_single_profile_by_user_id, get_single_setting_by_user_id, update_profile_by_user_id
from modules.utils.net import process_phone_number
from modules.utils.tools import process_schema_dictionary
from fastapi_pagination.ext.sqlalchemy import paginate
from settings.constants import USER_TYPES
from modules.utils.auth import AuthHandler

auth = AuthHandler()

def create_a_new_user(db: Session, username: str = None, email: str = None, phone_number: str = None, password: str = None, role: int = 0, first_name: str = None, other_name: str = None, last_name: str = None):
    country = get_single_country_by_code(db=db, code="NG")
    if role == 0:
        return {
            "status": False,
            "message": "Please select a role",
            'data': None
        }
    if role > 3:
        return {
            "status": False,
            "message": "Invalid role selected",
            'data': None
        }
    username = str(username).strip().replace(" ", "")
    processed_phone_number = process_phone_number(phone_number=phone_number, country_code=country.code)
    new_phone = None
    if processed_phone_number['status'] == True:
        new_phone = processed_phone_number['phone_number']
    else:
        new_phone = phone_number
    user_type = USER_TYPES['admin']['num']
    check = registration_unique_field_check(db=db, phone_number=new_phone, username=username, email=email, user_type=user_type)
    if check['status'] == False:
        return {
            'status': False,
            'message': check['message'],
            'data': None,
        }
    else:
        user = create_user_with_relevant_rows(db=db, country_id=country.id, username=username, email=email, phone_number=new_phone, password=password, user_type=user_type, role=role, first_name=first_name, other_name=other_name, last_name=last_name)
        return {
            'status': True,
            'message': "User created successfully",
            'data': get_main_single_user_by_id(db=db, id=user.id),
        }

def update_user_details(db: Session, user_id: int = 0, values: Dict = {}):
    values = process_schema_dictionary(info=values)
    user_values = {}
    profile_values = {}
    if 'status' in values:
        user_values['status'] = values['status']
    if 'role' in values:
        user_values['role'] = values['role']
    if 'first_name' in values:
        profile_values['first_name'] = values['first_name']
    if 'other_name' in values:
        profile_values['other_name'] = values['other_name']
    if 'last_name' in values:
        profile_values['last_name'] = values['last_name']
    if 'bio' in values:
        profile_values['bio'] = values['bio']
    if user_values != {}:
        update_user(db=db, id=user_id, values=user_values)
    if profile_values != {}:
        update_profile_by_user_id(db=db, user_id=user_id, values=profile_values)
    return {
        'status': True,
        'message': 'User updated successfully',
    }

def manage_user_password(db: Session, user_id: int = 0, password: str = None):
    password = auth.get_password_hash(password=password)
    da = {
        'password': password
    }
    update_user(db=db, id=user_id, values=da)
    return {
        'status': True,
        'message': 'Success'
    }

def retrieve_users(db: Session):
    users = get_users(db=db, filters={'user_type': USER_TYPES['admin']['num']})
    return paginate(users)

def retrieve_users_by_search(db: Session, filters: Dict={}):
    users = search_users(db=db, filters=filters)
    return paginate(users)

def retrieve_single_user(db: Session, user_id: int = 0):
    user = get_main_single_user_by_id(db=db, id=user_id)
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