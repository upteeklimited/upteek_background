from typing import Dict
from modules.external.api import send_external_request
from settings.config import load_env_config

config = load_env_config()

def make_squadco_request(endpoint: str=None, data: Dict={}, request_type: int=1):
    global config
    if data is None:
        data = {}
    url = config['squadco_url'] + endpoint
    headers = {
        'Authorization': 'Bearer ' + config['squadco_secret_key'],
        'Content-Type': 'application/json',
    }
    return send_external_request(url=url, headers=headers, data=data, type=request_type, https=True)

def squad_create_customer_virtual_account(first_name: str=None, last_name: str=None, middle_name: str=None, mobile_num: str=None, dob: str=None, email: str=None, bvn: str=None, gender: int=0, address: str=None, customer_identifier: str=None):
    endpoint = "virtual-account"
    data ={
        'first_name': first_name,
        'last_name': last_name,
        'dob': dob,
        'mobile_num': mobile_num,
        'bvn': bvn,
        'gender': gender,
        'address': address,
        'customer_identifier': customer_identifier,
    }
    if middle_name is not None:
        data['middle_name'] = middle_name
    if email is not None:
        data['email'] = email
    return make_squadco_request(endpoint=endpoint, data=data, request_type=2)

def squad_virtual_account_webhook_logs():
    endpoint = "virtual-account/webhook/logs"
    return make_squadco_request(endpoint=endpoint)

def squad_customer_virtual_account_transactions(customer_identifier: str=None):
    endpoint = "virtual-account/customer/transactions/" + str(customer_identifier)
    return make_squadco_request(endpoint=endpoint)

def squad_virtual_accounts_transactions():
    endpoint = "virtual-account/merchant/transactions"
    return make_squadco_request(endpoint=endpoint)

def squad_virtual_accounts_transactions_filters(page: int=0, perPage: int=0, virtualAccount: str=None, customerIdentifier: str=None, startDate: str=None, endDate: str=None, transactionReference: str=None, session_id: str=None):
    endpoint = "virtual-account/merchant/transactions/all"
    data = {}
    if page is not None:
        data['page'] = page
    if perPage is not None:
        data['perPage'] = perPage
    if virtualAccount is not None:
        data['virtualAccount'] = virtualAccount
    if customerIdentifier is not None:
        data['customerIdentifier'] = customerIdentifier
    if startDate is not None:
        data['startDate'] = startDate
    if endDate is not None:
        data['endDate'] = endDate
    if transactionReference is not None:
        data['transactionReference'] = transactionReference
    if session_id is not None:
        data['session_id'] = session_id
    return make_squadco_request(endpoint=endpoint, data=data)

def squad_virtual_account_customer_details_by_account_number(account_number: str=None):
    endpoint = "virtual-account/customer/" + str(account_number)
    return make_squadco_request(endpoint=endpoint)

def squad_virtual_account_customer_details_by_account_number(customer_identifier: str=None):
    endpoint = "virtual-account/" + str(customer_identifier)
    return make_squadco_request(endpoint=endpoint)

def squad_virtual_account_update_bvn(customer_bvn: str=None, customer_identifier: str=None, phone_number: str=None):
    endpoint = "virtual-account/update/bvn"
    data ={
        'customer_bvn': customer_bvn,
        'phone_number': phone_number,
        'customer_identifier': customer_identifier,
    }
    return make_squadco_request(endpoint=endpoint, data=data, request_type=6)

def squad_all_virtual_accounts(page: int=0, perPage: int=0, startDate: str=None, endDate: str=None):
    endpoint = "virtual-account/merchant/transactions/all"
    data = {}
    if page is not None:
        data['page'] = page
    if perPage is not None:
        data['perPage'] = perPage
    if startDate is not None:
        data['startDate'] = startDate
    if endDate is not None:
        data['endDate'] = endDate
    return make_squadco_request(endpoint=endpoint, data=data)

def squad_payout_account_lookup(bank_code: str=None, account_number: str=None):
    endpoint = "payout/account/lookup"
    data = {
        'bank_code': bank_code,
        'account_number': account_number,
    }
    return make_squadco_request(endpoint=endpoint, data=data, request_type=2)

def squad_payout_transfer(transaction_reference: str=None, amount: float=0, bank_code: str=None, account_number: str=None, account_name: str=None, remark: str=None):
    endpoint = "payout/transfer"
    data = {
        'transaction_reference': transaction_reference,
        'amount': str(amount*100),
        'bank_code': bank_code,
        'account_number': account_number,
        'account_name': account_name,
        'currency_id': 'NGN',
        'remark': remark,
    }
    return make_squadco_request(endpoint=endpoint, data=data, request_type=2)

def squad_payout_requery(transaction_reference: str=None):
    endpoint = "payout/requery"
    data = {
        'transaction_reference': transaction_reference,
    }
    return make_squadco_request(endpoint=endpoint, data=data, request_type=2)

def squad_payout_list(page: int=0, perPage: int=0, dir: str=None):
    endpoint = "payout/list"
    data = {}
    if page is not None:
        data['page'] = page
    if perPage is not None:
        data['perPage'] = perPage
    if dir is not None:
        data['dir'] = dir
    return make_squadco_request(endpoint=endpoint, data=data)

def squad_wallet_balance():
    endpoint = "merchant/balance"
    data = {
        'currency_id': 'NGN',
    }
    return make_squadco_request(endpoint=endpoint, data=data)

def squad_bill_airtime_vending(phone_number: str=None, amount: float=0):
    endpoint = "vending/purchase/airtime"
    data = {
        'phone_number': phone_number,
        'amount': amount,
    }
    return make_squadco_request(endpoint=endpoint, data=data, request_type=2)

def squad_bill_data_vending(phone_number: str=None, plan_code: str=None):
    endpoint = "vending/purchase/data"
    data = {
        'phone_number': phone_number,
        'plan_code': plan_code,
    }
    return make_squadco_request(endpoint=endpoint, data=data, request_type=2)

def squad_bill_get_data_bundles(network: str=None):
    endpoint = "vending/data-bundles"
    data = {
        'network': network,
    }
    return make_squadco_request(endpoint=endpoint, data=data)

def squad_bill_transactions(page: int=0, perPage: int=0, action: str=None):
    endpoint = "vending/transactions"
    data = {}
    if page is not None:
        data['page'] = page
    if perPage is not None:
        data['perPage'] = perPage
    if action is not None:
        data['action'] = action
    return make_squadco_request(endpoint=endpoint, data=data)
