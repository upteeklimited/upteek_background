from typing import Dict
from fastapi import Request
from database.model import get_single_user_by_email_and_user_type, get_single_user_by_phone_number_and_user_type, get_single_user_by_username_user_type, get_single_user_by_any_main_details, get_single_profile_by_user_id, get_single_setting_by_user_id, update_user, create_token, get_latest_user_token_by_type, update_token_by_user_id_and_token_type, update_token_email, get_latest_user_token_by_type_and_status, get_single_user_by_id, update_token, get_single_system_configuration_by_name, get_single_account_type_by_account_code, get_single_financial_product_by_id, create_account, get_last_account
from modules.utils.net import get_ip_info, process_phone_number
from modules.utils.tools import process_schema_dictionary
from modules.utils.auth import AuthHandler, get_next_few_minutes, check_if_time_as_pass_now
from modules.utils.acct import generate_internal_account_number
from modules.messaging.email import e_send_token
from sqlalchemy.orm import Session
import random
import datetime
import random
import sys, traceback
from settings.constants import USER_TYPES

auth = AuthHandler()

def generate_new_user_account(db: Session, user_id: int=0, merchant_id: int=0, account_name: str=None, is_merchant: bool=False, commit: bool=False):
    system_config = None
    if is_merchant == True:
        system_config = get_single_system_configuration_by_name(db=db, name="merchant_default_savings_account_code")
    else:
        system_config = get_single_system_configuration_by_name(db=db, name="customer_default_savings_account_code")
    if system_config is None:
        return {
            'status': False,
            'message': 'System Configuration not found',
            'data': None,
        }
    else:
        account_type_code = system_config.single_value
        account_type = get_single_account_type_by_account_code(db=db, account_code=account_type_code)
        if account_type is None:
            return {
                'status': False,
                'message': 'Account Type not found',
                'data': None,
            }
        else:
            account_type_id = account_type.id
            financial_product = get_single_financial_product_by_id(db=db, id=account_type.product_id)
            if financial_product is None:
                return {
                    'status': False,
                    'message': 'Financial Product not found',
                    'data': None
                }
            else:
                last_account_id = 0
                last_account = get_last_account(db=db)
                if last_account is not None:
                    last_account_id = last_account.id
                account_number = generate_internal_account_number(product_type=financial_product.product_type, last_id=last_account_id)
                account = create_account(db=db, user_id=user_id, merchant_id=merchant_id, account_type_id=account_type_id, account_name=account_name, account_number=account_number, is_primary=1, status=1, commit=commit)
                return {
                    'status': True,
                    'message': 'Account Created',
                    'data': account
                }

def login_with_email(db: Session, email: str=None, password: str=None, fbt: str=None):
    try:
        user = get_single_user_by_email_and_user_type(db=db, email=email, user_type=USER_TYPES['admin']['num'])
        if user is None:
            return {
                'status': False,
                'message': 'Email not correct',
                'data': None
            }
        else:
            if not auth.verify_password(plain_password=password, hashed_password=user.password):
                return {
                    'status': False,
                    'message': 'Password Incorrect',
                    'data': None
                }
            else:
                if user.status == 0:
                    return {
                        'status': False,
                        'message': 'This account has been locked',
                        'data': None
                    }
                if user.deleted_at is not None:
                    return {
                        'status': False,
                        'message': 'This account has been deactivated',
                        'data': None
                    }
                payload = {
                    'id': user.id,
                    'country_id': user.country_id,
                    'username': user.username,
                    'phone_number': user.phone_number,
                    'user_type': user.user_type,
                    'role': user.role,
                }
                token = auth.encode_token(user=payload, device_token=fbt)
                da = {
                    'device_token': fbt
                }
                update_user(db=db, id=user.id, values=da)
                profile = get_single_profile_by_user_id(db=db, user_id=user.id)
                setting = get_single_setting_by_user_id(db=db, user_id=user.id)
                data = {
                    'access_token': token,
                    'id': user.id,
                    'username': user.username,
                    'phone_number': user.phone_number,
                    'email': user.email,
                    'user_type': user.user_type,
                    'role': user.role,
                    'profile': profile,
                    'setting': setting,
                }
                return {
                    'status': True,
                    'message': 'Login Success',
                    'data': data,
                }
    except Exception as e:
        err = "Stack Trace - %s \n" % (traceback.format_exc())
        return {
            'status': False,
            'message': err,
            'data': None
        }

def send_email_token(db: Session, email: str=None):
    update_token_email(db=db, email=email, values={'status': 2})
    minutes = 10
    expired_at = get_next_few_minutes(minutes=minutes)
    token = str(random.randint(100000,999999))
    create_token(db=db, email=email, token_type="email", token_value=token, status=0, expired_at=expired_at)
    e_send_token(username="Upteek User", email=email, token=token, minutes=minutes)
    return {
        'status': True,
        'message': 'Success',
    }
    
def send_user_email_token(db: Session, email: str=None):
    user = get_single_user_by_email_and_user_type(db=db, email=email, user_type=USER_TYPES['admin']['num'])
    if user is None:
        return {
            'status': False,
            'message': 'Email not correct',
        }
    else:
        update_token_by_user_id_and_token_type(db=db, user_id=user.id, token_type="email", values={'status': 2})
        minutes = 10
        expired_at = get_next_few_minutes(minutes=minutes)
        token = str(random.randint(100000,999999))
        create_token(db=db, user_id=user.id, email=email, token_type="email", token_value=token, status=0, expired_at=expired_at)
        e_send_token(username=user.username, email=email, token=token, minutes=minutes)
        return {
            'status': True,
            'message': 'Success',
        }

def finalise_passwordless_login(db: Session, email: str=None, token_str: str=None, fbt: str=None):
    user = get_single_user_by_email_and_user_type(db=db, email=email, user_type=USER_TYPES['admin']['num'])
    if user is None:
        return {
            'status': False,
            'message': 'Email not correct',
            'data': None
        }
    else:
        token = get_latest_user_token_by_type_and_status(db=db, user_id=user.id, token_type="email", status=0)
        if token is None:
            return {
                'status': False,
                'message': 'User has no pending email token',
                'data': None
            }
        else:
            if token.status != 0:
                return {
                    'status': False,
                    'message': 'Token already used',
                    'data': None
                }
            if token.token_value != token_str:
                return {
                    'status': False,
                    'message': 'Invalid Token Value',
                    'data': None
                }
            if check_if_time_as_pass_now(time_str=token.expired_at) == True:
                update_token(db=db, id=token.id, values={'status': 2})
                return {
                    'status': False,
                    'message': 'Token has expired',
                    'data': None
                }
            if user.status == 0:
                return {
                    'status': False,
                    'message': 'This account has been locked',
                    'data': None
                }
            if user.deleted_at is not None:
                return {
                    'status': False,
                    'message': 'This account has been deactivated',
                    'data': None
                }
            payload = {
                'id': user.id,
                'country_id': user.country_id,
                'username': user.username,
                'phone_number': user.phone_number,
                'user_type': user.user_type,
                'role': user.role,
            }
            access_token = auth.encode_token(user=payload, device_token=fbt)
            da = {
                'device_token': fbt
            }
            update_user(db=db, id=user.id, values=da)
            update_token(db=db, id=token.id, values={'status': 1})
            profile = get_single_profile_by_user_id(db=db, user_id=user.id)
            setting = get_single_setting_by_user_id(db=db, user_id=user.id)
            data = {
                'access_token': access_token,
                'id': user.id,
                'username': user.username,
                'phone_number': user.phone_number,
                'email': user.email,
                'user_type': user.user_type,
                'role': user.role,
                'profile': profile,
                'setting': setting,
            }
            return {
                'status': True,
                'message': 'Login Success',
                'data': data,
            }

def verify_email_token(db: Session, email: str=None, token_str: str=None):
    user = get_single_user_by_email_and_user_type(db=db, email=email, user_type=USER_TYPES['admin']['num'])
    if user is None:
        return {
            'status': False,
            'message': 'Email not correct',
        }
    else:
        token = get_latest_user_token_by_type_and_status(db=db, user_id=user.id, token_type="email", status=0)
        if token is None:
            return {
                'status': False,
                'message': 'User has no pending email token',
            }
        else:
            if token.status != 0:
                return {
                    'status': False,
                    'message': 'Token already used',
                }
            if token.token_value != token_str:
                return {
                    'status': False,
                    'message': 'Invalid Token Value',
                }
            if check_if_time_as_pass_now(time_str=token.expired_at) == True:
                update_token(db=db, id=token.id, values={'status': 2})
                return {
                    'status': False,
                    'message': 'Token has expired',
                }
            update_token(db=db, id=token.id, values={'status': 1})
            return {
                'status': True,
                'message': 'Success'
            }

def get_user_details(db: Session, user_id: int=0):
    user = get_single_user_by_id(db=db, id=user_id)
    if user is None:
        return {
            'status': False,
            'message': 'User not found',
            'data': None
        }
    else:
        profile = get_single_profile_by_user_id(db=db, user_id=user.id)
        setting = get_single_setting_by_user_id(db=db, user_id=user.id)
        data = {
            'id': user.id,
            'username': user.username,
            'phone_number': user.phone_number,
            'email': user.email,
            'user_type': user.user_type,
            'role': user.role,
            'profile': profile,
            'setting': setting,
        }
        return {
            'status': True,
            'message': 'Success',
            'data': data,
        }

# async def sso_google(request: Request):
#     token = await oauth.google.authorize_access_token(request)
#     user_info = token.get('userinfo')
