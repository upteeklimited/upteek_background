from typing import Dict
from modules.external.api import send_external_request
from settings.config import load_env_config

config = load_env_config()

def make_fw_request(endpoint: str=None, data: Dict={}, request_type: int=1):
    global config
    if data is None:
        data = {}
    url = config['flutterwave_url'] + endpoint
    headers = {
        'Authorization': 'Bearer ' + config['flutterwave_secret_key'],
        'Content-Type': 'application/json',
    }
    return send_external_request(url=url, headers=headers, data=data, type=request_type, https=True)


def fw_get_bill_categories(airtime: int = None, data_bundle: int = None, internet: int = None, power: int = None, cables: int = None, toll: int = None, biller_code: str = None):
    endpoint = "get_bill_categories"
    data = {}
    if airtime is not None:
        data['airtime'] = airtime
    if data_bundle is not None:
        data['data_bundle'] = data_bundle
    if internet is not None:
        data['internet'] = internet
    if power is not None:
        data['power'] = power
    if cables is not None:
        data['cables'] = cables
    if toll is not None:
        data['toll'] = toll
    if biller_code is not None:
        data['biller_code'] = biller_code
    return make_fw_request(endpoint=endpoint, data=data, request_type=1)

def fw_validate_bill(item_code: str = None, code: str = None, customer: str = None):
    endpoint = "validate_bill"
    data = {
        'item_code': item_code,
        'code': code,
        'customer': customer,
    }
    return make_fw_request(endpoint=endpoint, data=data, request_type=2)

def fw_pay_bill(country: str = None, customer: str = None, amount: float = 0, type: str = None):
    endpoint = "pay_bill"
    data = {
        'country': country,
        'customer': customer,
        'amount': amount,
        'type': type,
    }
    return make_fw_request(endpoint=endpoint, data=data, request_type=2)

def fw_transaction_status(ref: str = None):
    endpoint = "get_bill_status/" + ref
    return make_fw_request(endpoint=endpoint, request_type=1)

def fw_verify_transaction_by_id(transaction_id: str=None):
    endpoint = "transactions/" + str(transaction_id) + "/verify"
    return make_fw_request(endpoint=endpoint, request_type=1)

def fw_verify_transaction_by_reference(reference: str=None):
    endpoint = "transactions/verify/"
    return make_fw_request(endpoint=endpoint, data={'tx_ref': reference}, request_type=1)