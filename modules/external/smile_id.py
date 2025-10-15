from typing import Dict
from smile_id_core import Signature, IdApi, ServerError, Utilities, WebApi
from smile_id_core.BusinessVerification import BusinessVerification
import hmac
import hashlib
import base64
import requests
import uuid
from datetime import datetime, timezone
from modules.utils.tools import generate_basic_reference, format_date_for_smile_id
from settings.config import load_env_config

config = load_env_config()

def generate_smile_id_signature():
    global config
    partner_id = config['smile_id_partner_id']
    api_key = config['smile_id_api_key']
    try:
        signature = Signature(partner_id, api_key)
        data = signature.generate_signature()
        return {
            'status': True,
            'message': 'Signature generated successfully',
            'data': data
        }
    except Exception as e:
        return {
            'status': False,
            'message': str(e),
            'data': None
        }

def generate_smile_id_v2_signature(job_id: str=None, timestamp: str=None):
    global config
    partner_id = config['smile_id_partner_id']
    api_key = config['smile_id_api_key']
    message = f"{partner_id}{job_id}{timestamp}".encode("utf-8")
    secret = api_key.encode("utf-8")
    signature = hmac.new(secret, message, hashlib.sha256).digest()
    return base64.b64encode(signature).decode("utf-8")

def do_basic_kyc_verification(payload: Dict={}):
    global config
    if payload is None:
        payload = {}
    if payload == {}:
        return {
            'status': False,
            'message': 'No ID information provided',
            'data': None
        }
    partner_id = config['smile_id_partner_id']
    job_id = str(uuid.uuid4())[:12]
    timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    signature = generate_smile_id_v2_signature(job_id=job_id, timestamp=timestamp)
    try:
        payload['partner_id'] = partner_id
        payload['partner_params']['job_id'] = job_id
        payload['timestamp'] = timestamp
        payload['signature'] = signature
        payload['source_sdk_version'] = "2.0.0"
        payload['source_sdk'] = "rest_api"
        payload['country'] = "NG"
        response = requests.post(
            config['smile_id_url'] + 'v2/verify',
            json=payload
        )
        if response.status_code == 200:
            data = response.json()
            return {
                'status': True,
                'message': 'Success',
                'data': data,
                'status_code': 200
            }
        else:
            return {
                'status': False,
                'message': 'Failed to verify ID',
                'data': None,
                'status_code': response.status_code
            }
    except Exception as e:
        return {
            'status': False,
            'message': str(e),
            'data': None
        }

def do_bvn_verification(bvn: str=None, first_name: str=None, last_name: str=None, phone_number: str=None, date_of_birth: str=None, user_id: str=None):
    if date_of_birth is not None:
        date_of_birth = format_date_for_smile_id(date_of_birth)
    payload = {
        "first_name": first_name,
        "id_number": bvn,
        "id_type": "BVN",
        "last_name": last_name,
        "partner_params": {
            "user_id": user_id
        },
        "phone_number": phone_number,
        "dob": date_of_birth,
    }
    return do_basic_kyc_verification(payload=payload)

def do_nin_verification(nin: str=None, first_name: str=None, last_name: str=None, phone_number: str=None, user_id: str=None):
    payload = {
        "first_name": first_name,
        "id_number": nin,
        "id_type": "NIN",
        "last_name": last_name,
        "partner_params": {
            "user_id": user_id
        },
        "phone_number": phone_number,
    }
    return do_basic_kyc_verification(payload=payload)

def verify_smile_id_signature(string_val: str=None, timestamp_val: str=None):
    global config
    partner_id = config['smile_id_partner_id']
    api_key = config['smile_id_api_key']
    try:
        signature = Signature(partner_id, api_key)
        verify = signature.confirm_signature(msg_signature=string_val, timestamp=timestamp_val)
        if verify == True:
            return {
                'status': True,
                'message': 'Signature verified successfully',
            }
        else:
            return {
                'status': False,
                'message': 'Signature verification failed',
            }
    except Exception as e:
        return {
            'status': False,
            'message': str(e),
        }
    

def do_enhanced_kyc_verification(id_info_params: Dict={}, user_id: str=None):
    global config
    if id_info_params is None:
        id_info_params = {}
    if id_info_params == {}:
        return {
            'status': False,
            'message': 'No ID information provided',
            'data': None
        }
    partner_id = config['smile_id_partner_id']
    api_key = config['smile_id_api_key']
    sid_server  = config['smile_id_server_type']
    
    job_id = generate_basic_reference(rand_size=15)
    partner_params = {
        'user_id': user_id,
        'job_id': job_id,
        'job_type': 5,
    }
    option_params = {
        "signature": True,
    }
    try:
        connection = IdApi(partner_id, api_key, sid_server)
        response = connection.submit_job(partner_params, id_info_params, options_params=option_params)
        return {
            'status': True,
            'message': 'Success',
            'data': response,
        }
    except ValueError as e:
        return {
            'status': False,
            'message': str(e),
            'data': None
        }
    except ServerError:
        return {
            'status': False,
            'message': 'Verification Server error',
            'data': None
        }
    except Exception as e:
        return {
            'status': False,
            'message': str(e),
            'data': None
        }

def do_business_kyb_verification(id_info_params: Dict={}, user_id: str=None):
    global config
    if id_info_params is None:
        id_info_params = {}
    if id_info_params == {}:
        return {
            'status': False,
            'message': 'No ID information provided',
            'data': None
        }
    partner_id = config['smile_id_partner_id']
    api_key = config['smile_id_api_key']
    sid_server  = config['smile_id_server_type']
    
    job_id = generate_basic_reference(rand_size=15)
    partner_params = {
        'user_id': user_id,
        'job_id': job_id,
        'job_type': 7,
    }
    try:
        connection = BusinessVerification(partner_id, api_key, sid_server)
        response = connection.submit_job(partner_params, id_info_params)
        return {
            'status': True,
            'message': 'Success',
            'data': response,
        }
    except ValueError as e:
        return {
            'status': False,
            'message': str(e),
            'data': None
        }
    except ServerError:
        return {
            'status': False,
            'message': 'Server error',
            'data': None
        }
    except Exception as e:
        return {
            'status': False,
            'message': str(e),
            'data': None
        }

def get_smile_id_job_status(job_id: str=None, user_id: int=0, return_all: bool=False, return_images: bool=False):
    global config
    partner_id = config['smile_id_partner_id']
    api_key = config['smile_id_api_key']
    sid_server  = config['smile_id_server_type']
    partner_params = {
        'user_id': str(user_id),
        'job_id': job_id,
        'job_type': 5,
    }
    options = {
    "return_job_status": True,
    "return_history": return_all,
    "return_images": return_images,
    "signature": True
    }
    try:
        connection = Utilities(partner_id, api_key, sid_server)
        response = connection.get_job_status(partner_params=partner_params, option_params=options)
        return {
            'status': True,
            'message': 'Success',
            'data': response,
        }
    except ValueError as e:
        return {
            'status': False,
            'message': str(e),
            'data': None
        }
    except ServerError:
        return {
            'status': False,
            'message': 'Server error',
            'data': None
        }
    except Exception as e:
        return {
            'status': False,
            'message': str(e),
            'data': None
        }
    
def generate_simle_id_web_token(user_id: int=0, product: str=None, callback_url: str=None):
    global config
    partner_id = config['smile_id_partner_id']
    api_key = config['smile_id_api_key']
    sid_server  = config['smile_id_server_type']
    try:
        connection = WebApi(partner_id,callback_url,api_key,sid_server)
        job_id = generate_basic_reference(rand_size=15)
        response = connection.get_web_token(str(user_id),job_id,product)
        if response['status'] != True:
            return {
                'status': False,
                'message': 'Generation failed',
                'data': None
            }
        else:
            data = {
                'token': response['token'],
                'job_id': job_id,
            }
            return {
                'status': True,
                'message': 'Success',
                'data': data
            }
    except ValueError as e:
        return {
            'status': False,
            'message': str(e),
            'data': None
        }
    except ServerError:
        return {
            'status': False,
            'message': 'Server error',
            'data': None
        }
    except Exception as e:
        return {
            'status': False,
            'message': str(e),
            'data': None
        }