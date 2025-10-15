from typing import Dict
from modules.external.api import send_external_request
from settings.config import load_env_config

config = load_env_config()

def make_paystack_request(endpoint: str=None, data: Dict={}, request_type: int=1):
    global config
    if data is None:
        data = {}
    url = config['paystack_url'] + endpoint
    headers = {
        'Authorization': 'Bearer ' + config['paystack_secret_key'],
        'Content-Type': 'application/json',
    }
    return send_external_request(url=url, headers=headers, data=data, type=request_type, https=True)

def paystack_get_banks():
    endpoint = "get_banking"
    return make_paystack_request(endpoint=endpoint, request_type=1)

def paystack_verify_name(bank_code: str = None, account_number: str = None):
    endpoint = "verify_name"
    data = {
        'bank_code': bank_code,
        'account_number': account_number,
    }
    return make_paystack_request(endpoint=endpoint, data=data, request_type=2)

def paystack_verify_transaction(reference: str = None):
    endpoint = "transaction/verify/" + reference
    return make_paystack_request(endpoint=endpoint, request_type=1)

def paystack_get_banks():
    endpoint = "bank"
    return make_paystack_request(endpoint=endpoint, request_type=1)

def paystack_resolve_account_number(account_number: str = None, bank_code: str = None):
    endpoint = "bank/resolve?" + "account_number=" + account_number + "&bank_code=" + bank_code
    return make_paystack_request(endpoint=endpoint, request_type=1)

def paystack_get_virtual_account_providers():
    endpoint = "dedicated_account/available_providers"
    return make_paystack_request(endpoint=endpoint, request_type=1)

def paystack_create_customer(first_name: str = None, last_name: str = None, email: str = None, phone: str = None):
    endpoint = "customer"
    data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': phone,
    }
    return make_paystack_request(endpoint=endpoint, data=data, request_type=2)

def paystack_update_customer(customer_id: str = None, first_name: str = None, last_name: str = None, email: str = None, phone: str = None):
    endpoint = "customer/" + customer_id
    data = {}
    if first_name is not None:
        data['first_name'] = first_name
    if last_name is not None:
        data['last_name'] = last_name
    if email is not None:
        data['email'] = email
    if phone is not None:
        data['phone'] = phone
    return make_paystack_request(endpoint=endpoint, data=data, request_type=4)

def paystack_get_list_of_customers():
    endpoint = "customer"
    return make_paystack_request(endpoint=endpoint, request_type=1)

def paystack_get_customer(customer_id: str = None):
    endpoint = "customer/" + customer_id
    return make_paystack_request(endpoint=endpoint, request_type=1)

def paystack_validate_customer(customer_id: str = None, first_name: str = None, other_name: str = None, last_name: str = None, type: str = None, value: str = None, country: str = None, bvn: str = None, bank_code: str = None, account_number: str = None):
    endpoint = "customer/" + str(customer_id) + "/validate"
    data = {
        'first_name': first_name,
        'middle_name': other_name,
        'last_name': last_name,
        'type': type,
        'value': value,
        'country': country,
        'bvn': bvn,
        'bank_code': bank_code,
        'account_number': account_number,
    }
    return make_paystack_request(endpoint=endpoint, data=data, request_type=2)

def paystack_customer_set_risk_action(customer_id: str = None, risk_action: str = None):
    endpoint = "customer/set_risk_action"
    data = {
        'customer': customer_id,
        'risk_action': risk_action,
    }
    return make_paystack_request(endpoint=endpoint, data=data, request_type=2)

def paystack_create_dedicated_virtual_account(customer_id: str = None, preferred_bank: str = None):
    endpoint = "dedicated_account"
    data = {
        'customer': customer_id,
        'preferred_bank': preferred_bank,
    }
    return make_paystack_request(endpoint=endpoint, data=data, request_type=2)

def paystack_assign_dedicated_virtual_account(email: str = None, first_name: str = None, last_name: str = None, phone: str = None, preferred_bank: str = None, country: str = None):
    endpoint = "dedicated_account/assign"
    data = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'phone': phone,
        'preferred_bank': preferred_bank,
        'country': country,
    }
    return make_paystack_request(endpoint=endpoint, data=data, request_type=2)

def paystack_list_dedicated_virtual_accounts():
    endpoint = "dedicated_account"
    return make_paystack_request(endpoint=endpoint, request_type=1)

def paystack_get_dedicated_virtual_account(account_id: str = None):
    endpoint = "dedicated_account/" + account_id
    return make_paystack_request(endpoint=endpoint, request_type=1)

def paystack_requery_dedicated_virtual_account(account_number: str = None, provider_slug: str = None, date: str = None):
    endpoint = "dedicated_account/requery?" + "account_number=" + account_number + "&provider_slug=" + provider_slug + "&date=" + date
    return make_paystack_request(endpoint=endpoint, request_type=1)

def paystack_deactivate_dedicated_virtual_account(account_id: str = None):
    endpoint = "dedicated_account/" + str(account_id)
    return make_paystack_request(endpoint=endpoint, request_type=5)

def paystack_create_transfer_recipient(type: str = None, name: str = None, account_number: str = None, bank_code: str = None, currency: str = None):
    endpoint = "transferrecipient"
    data = {
        'type': type,
        'name': name,
        'account_number': account_number,
        'bank_code': bank_code,
        'currency': currency,
    }
    return make_paystack_request(endpoint=endpoint, data=data, request_type=2)

def paystack_update_transfer_recipient(recipient_id: str = None, type: str = None, name: str = None, account_number: str = None, bank_code: str = None, currency: str = None):
    endpoint = "transferrecipient/" + recipient_id
    data = {}
    if type is not None:
        data['type'] = type
    if name is not None:
        data['name'] = name
    if account_number is not None:
        data['account_number'] = account_number
    if bank_code is not None:
        data['bank_code'] = bank_code
    if currency is not None:
        data['currency'] = currency
    return make_paystack_request(endpoint=endpoint, data=data, request_type=4)

def paystack_delete_transfer_recipient(recipient_id: str = None):
    endpoint = "transferrecipient/" + recipient_id
    return make_paystack_request(endpoint=endpoint, request_type=5)

def paystack_list_transfer_recipients():
    endpoint = "transferrecipient"
    return make_paystack_request(endpoint=endpoint, request_type=1)

def paystack_get_transfer_recipient(recipient_id: str = None):
    endpoint = "transferrecipient/" + recipient_id
    return make_paystack_request(endpoint=endpoint, request_type=1)

def paystack_initiate_transfer(recipient: str = None, amount: float = 0, currency: str = "NGN", reference: str = None, reason: str = None):
    endpoint = "transfer"
    data = {
        'recipient': recipient,
        'amount': (amount * 100),  # Paystack expects amount in kobo
        'currency': currency,
        'reference': reference,
        'reason': reason,
        'source': 'balance',
    }
    return make_paystack_request(endpoint=endpoint, data=data, request_type=2)

def paystack_finalize_transfer(transfer_code: str = None, otp: str = None):
    endpoint = "transfer/finalize_transfer"
    data = {
        'transfer_code': transfer_code,
        'otp': otp,
    }
    return make_paystack_request(endpoint=endpoint, data=data, request_type=2)

def paystack_verify_transfer(reference: str = None):
    endpoint = "transfer/verify/" + reference
    return make_paystack_request(endpoint=endpoint, request_type=1)