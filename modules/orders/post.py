from typing import Dict, List, Any
from sqlalchemy.orm import Session
from database.model import create_order, update_order, create_order_product, create_transaction, get_single_user_primary_account, get_addressable, debit_account, credit_general_ledger_account, get_single_general_ledger_account_by_account_number, get_single_system_configuration_by_name, get_single_merchant_by_id, update_transaction, get_single_currency_by_code, get_single_order_by_id, create_order_log, get_single_user_by_id
from modules.utils.tools import process_schema_dictionary, generate_transaction_reference, generate_order_reference, order_pin
from modules.transactions.trans import process_account_order


def create_new_order(db: Session, user_id: int=0, country_id: int=0, merchant_id: int=0, address_id: int=0, is_account: bool=False, is_card: bool=False, card_id: int=0, card_transaction_reference: str=None, save_card: bool=False, provider_code: str=None, products: List=[], amount: float=0, discount: float=0, total_amount: float=0, delivery_status: int=0, status: int=0, commit: bool=False):
    # merchant = get_single_merchant_by_id(db=db, id=merchant_id)
    currency = get_single_currency_by_code(db=db, code="NGN")
    currency_id = 0
    # if merchant is not None:
    #     currency_id = merchant.currency_id
    if currency is not None:
        currency_id = currency.id
    user = get_single_user_by_id(db=db, id=user_id)
    if user is None:
        return {
            'status': False,
            'message': 'User not found',
            'data': None
        }
    main_trans = None
    payment_type = 0
    processor = None
    if is_account == True:
        processor = process_account_order(db=db, user_id=user_id, country_id=country_id, merchant_id=merchant_id, amount=total_amount, commit=commit)
        payment_type = 2
    # elif is_card == True:
    #     processor = process_card_order(db=db, user_id=user_id, country_id=country_id, merchant_id=merchant_id, provider_code=provider_code, amount=total_amount, external_reference=card_transaction_reference, save_card=save_card, card_id=card_id)
    #     payment_type = 1
    if processor is None:
        return {
            'status': False,
            'message': 'Transaction failed',
            'data': None
        }
    if processor['status'] == False:
        return {
            'status': False,
            'message': processor['message'],
            'data': None
        }
    main_trans = processor['data']
    reference = generate_order_reference()
    order = create_order(db=db, user_id=user_id, merchant_id=merchant_id, currency_id=currency_id, card_id=main_trans.card_id, account_id=main_trans.account_id, reference=reference, sub_total=amount, total_amount=total_amount, discount=discount, address_id=address_id, payment_type=payment_type, pick_up_pin=order_pin(), delivery_pin=order_pin(), payment_status=1, delivery_status=delivery_status, status=status, commit=commit)
    # product_ids = []
    if len(products) > 0:
        for product in products:
            # product_ids.append(product['product_id'])
            create_order_product(db=db, product_id=product['product_id'], order_id=order.id, quantity=product['quantity'], amount=product['amount'], status=1, commit=commit)
    update_transaction(db=db, id=main_trans.id, values={'order_id': order.id}, commit=commit)
    data = get_single_order_by_id(db=db, id=order.id)
    return {
        'status': True,
        'message': 'Success',
        'data': data
    }
