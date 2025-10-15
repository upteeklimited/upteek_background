from typing import Dict
import jwt 
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext 
from datetime import datetime, timedelta, UTC
import dateparser
import time
from settings.config import load_env_config
from database.model import create_auth_token, get_latest_user_auth_token, get_single_user_by_id, update_auth_token, update_user_auth_token
from database.db import session, has_uncommitted_changes, get_laravel_datetime
from sqlalchemy.orm import Session
import hashlib
import json
from settings.constants import USER_TYPES
from authlib.integrations.starlette_client import OAuth
from authlib.jose import jwt as auth_jwt

config = load_env_config()

# def generate_apple_client_secret():
#     global config
#     now = datetime.now(UTC)
#     payload = {
#         'iss': config['apple_team_id'],
#         'iat': now,
#         'exp': now + timedelta(days=180),
#         'aud': 'https://appleid.apple.com',
#         'sub': config['apple_client_id']
#     }
#     headers = {
#         'alg': 'ES256',
#         'kid': config['apple_key_id']
#     }
#     key = config['apple_private_key']
#     return auth_jwt.encode(headers, payload, key).decode('utf-8')

# Initialize OAuth
# oauth = OAuth()

# # Register OAuth providers
# oauth.register(
#     name='google',
#     client_id=config['google_client_id'],
#     client_secret=config['google_client_secret'],
#     server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
#     client_kwargs={
#         'scope': 'openid email profile',
#         'prompt': 'select_account',  # Forces account selection
#     },
#     authorize_params={
#         'access_type': 'offline',  # For refresh tokens
#     }
# )

# oauth.register(
#     name='facebook',
#     client_id=config['facebook_client_id'],
#     client_secret=config['facebook_client_secret'],
#     authorize_url='https://www.facebook.com/v12.0/dialog/oauth',
#     access_token_url='https://graph.facebook.com/v12.0/oauth/access_token',
#     api_base_url='https://graph.facebook.com/v12.0/',
#     client_kwargs={
#         'scope': 'email public_profile',
#         'token_endpoint_auth_method': 'client_secret_post'  # Facebook requires this
#     }
# )

# # Apple requires special handling
# oauth.register(
#     name='apple',
#     client_id=config['apple_client_id'],  # Service ID from Apple Developer
#     client_secret=generate_apple_client_secret(),  # Generated JWT (see below)
#     authorize_url='https://appleid.apple.com/auth/authorize',
#     access_token_url='https://appleid.apple.com/auth/token',
#     api_base_url='https://appleid.apple.com',
#     client_kwargs={
#         'scope': 'email name',
#         'response_mode': 'form_post'  # Apple requires POST for auth response
#     }
# )

def get_next_few_minutes(minutes: int=0):
    current_time = datetime.now()
    future_time = current_time + timedelta(minutes=minutes)
    return future_time.strftime("%Y-%m-%d %H:%M:%S")

def check_if_time_as_pass_now(time_str: str = None):
    date_parsed = dateparser.parse(str(time_str), date_formats=['%d-%m-%Y %H:%M:%S'])
    time_tz = time.mktime(date_parsed.timetuple())
    time_tz = int(time_tz)
    current_tz = int(time.time())
    if current_tz >= time_tz:
        return True
    else:
        return False

class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = config['secret_key']
    db = session

    def get_password_hash(self, password: str = None):
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str=None, hashed_password: str=None):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user: Dict={}, device_token: str = None):
        payload = {
            'exp': datetime.now() + timedelta(days=365, minutes=5),
            'iat': datetime.now(),
            'sub': json.dumps(user)
        }
        expired_at = (datetime.now() + timedelta(days=365, minutes=5)).strftime("%Y/%m/%d %H:%M:%S")
        token = jwt.encode(payload, self.secret, algorithm="HS256")
        user_id = user['id']
        update_user_auth_token(db=self.db, user_id=user_id, values={'status': 0}, commit=True)
        create_auth_token(db=self.db, user_id=user_id, token=token, device_token=device_token, status=1, expired_at=expired_at, commit=True)
        return token

    def decode_token(self, token: str = None):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            sub_data = json.loads(payload['sub'])
            user_id = sub_data['id']
            user = get_single_user_by_id(db=self.db, id=user_id)
            if user is None:
                raise HTTPException(status_code=401, detail='User does not exist')
            else:
                auth_token = get_latest_user_auth_token(db=self.db, user_id=user_id)
                if auth_token is None:
                    raise HTTPException(status_code=401, detail='Empty Auth Token')
                else:
                    if auth_token.token != token:
                        raise HTTPException(status_code=401, detail='Invalid Auth Token')
                    else:
                        if auth_token.status == 0:
                            raise HTTPException(status_code=401, detail='Token Expired')
                        else:
                            if user.user_type != USER_TYPES['admin']['num']:
                                raise HTTPException(status_code=401, detail='Invalid User Type')
                            deleted_at = user.deleted_at
                            if deleted_at is not None:
                                raise HTTPException(status_code=401, detail='User is deleted')
                            else:
                                update_auth_token(db=self.db, id=auth_token.id, values={'last_ping_at': get_laravel_datetime()}, commit=True)
                                return sub_data
        
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

    def auth_admin_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        user = self.decode_token(auth.credentials)
        return user
    
    def auth_super_admin_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        user = self.decode_token(auth.credentials)
        if user['role'] != USER_TYPES['admin']['roles']['super']['num']:
            raise HTTPException(status_code=401, detail="Resource not available for this role")
        return user
    
    def auth_authorizer_admin_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        user = self.decode_token(auth.credentials)
        if user['role'] != USER_TYPES['admin']['roles']['auth']['num']:
            raise HTTPException(status_code=401, detail="Resource not available for this role")
        return user
    
    def auth_entry_admin_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        user = self.decode_token(auth.credentials)
        if user['role'] != USER_TYPES['admin']['roles']['entry']['num']:
            raise HTTPException(status_code=401, detail="Resource not available for this role")
        return user
    
    # def auth_user_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
    #     user = self.decode_token(auth.credentials)
    #     return user
