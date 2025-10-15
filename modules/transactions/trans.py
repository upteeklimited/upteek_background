from typing import Dict
import dateparser
from sqlalchemy.orm import Session
from database.model import debit_account, create_account, debit_general_ledger_account, credit_general_ledger_account, credit_account, create_transaction, get_single_account_by_account_number, get_single_general_ledger_account_by_account_number, get_single_transaction_type_by_id, get_single_currency_by_code, get_single_country_by_code, get_single_transaction_by_id, get_single_user_primary_account, get_single_merchant_by_id, get_single_system_configuration_by_name, get_single_transaction_type_by_code
from modules.utils.tools import generate_transaction_reference, process_schema_dictionary
from settings.constants import TRANSACTION_ACTIONS


def create_general_posting(db: Session, transaction_type_id: int=0, from_account_number: str=None, to_account_number: str=None, amount: float=0, narration: str=None, commit: bool=False):
    country_id = 0
    country = get_single_country_by_code(db=db, code="NG")
    if country is not None:
        country_id = country.id
    currency_id = 0
    currency = get_single_currency_by_code(db=db, code="NGN")
    if currency is not None:
        currency_id = currency.id
    transaction_type = get_single_transaction_type_by_id(db=db, id=transaction_type_id)
    if transaction_type is None:
        return {
            'status': False,
            'message': 'Transaction type not found',
            'data': None,
        }
    else:
        reference = generate_transaction_reference(tran_type=transaction_type.name)
        from_gl = get_single_general_ledger_account_by_account_number(db=db, account_number=from_account_number)
        to_gl = get_single_general_ledger_account_by_account_number(db=db, account_number=to_account_number)
        from_acct = get_single_account_by_account_number(db=db, account_number=from_account_number)
        to_acct = get_single_account_by_account_number(db=db, account_number=to_account_number)
        main_trans = None
        from_done = False
        to_done = False
        type_action= transaction_type.action
        if type_action == 1:
            if from_gl is not None:
                dg_prev_balance = from_gl.balance
                dgl = debit_general_ledger_account(db=db, general_ledger_account_id=from_gl.id, amount=amount, commit=commit)
                if dgl['status'] == False:
                    return {
                        'status': False,
                        'message': dgl['message'],
                        'data': None
                    }
                else:
                    main_trans = create_transaction(db=db, country_id=country_id, currency_id=currency_id, gl_id=from_gl.id, type_id=transaction_type_id, action=TRANSACTION_ACTIONS['debit'], reference=reference, description=narration, narration=narration, amount=amount, previous_balance=dg_prev_balance, new_balance=dgl['data']['balance'], status=1, commit=commit)
                    from_done = True
            if from_acct is not None:
                da_prev_balance = from_acct.available_balance
                da = debit_account(db=db, account_id=from_acct.id, amount=amount, override=True, commit=commit)
                if da['status'] == False:
                    return {
                        'status': False,
                        'message': da['message'],
                        'data': None
                    }
                main_trans = create_transaction(db=db, country_id=country_id, currency_id=currency_id, user_id=from_acct.user_id, merchant_id=from_acct.merchant_id, account_id=from_acct.id, type_id=transaction_type_id, action=TRANSACTION_ACTIONS['debit'], reference=reference, description=narration, narration=narration, amount=amount, previous_balance=da_prev_balance, new_balance=da['data']['available_balance'], status=1, commit=commit)
                from_done = True
            if to_gl is not None:
                cgl_prvebalance = to_gl.balance
                cgl = credit_general_ledger_account(db=db, general_ledger_account_id=to_gl.id, amount=amount, commit=commit)
                if cgl['status'] == False:
                    return {
                        'status': False,
                        'message': cgl['message'],
                        'data': None
                    }
                create_transaction(db=db, country_id=country_id, currency_id=currency_id, gl_id=to_gl.id, type_id=transaction_type_id, action=TRANSACTION_ACTIONS['credit'], reference=reference, description=narration, narration=narration, amount=amount, previous_balance=cgl_prvebalance, new_balance=cgl['data']['balance'], status=1, commit=commit)
                to_done = True
            if to_acct is not None:
                ca_prev_balance = to_acct.available_balance
                ca = credit_account(db=db, account_id=to_acct.id, amount=amount, commit=commit)
                if ca['status'] == False:
                    return {
                        'status': False,
                        'message': ca['message'],
                        'data': None
                    }
                create_transaction(db=db, country_id=country_id, currency_id=currency_id, user_id=to_acct.user_id, merchant_id=to_acct.merchant_id, account_id=to_acct.id, type_id=transaction_type_id, action=TRANSACTION_ACTIONS['credit'], reference=reference, description=narration, narration=narration, amount=amount, previous_balance=ca_prev_balance, new_balance=ca['data']['available_balance'], status=1, commit=commit)
                to_done = True
        elif type_action == 2:
            if from_gl is not None:
                dg_prev_balance = from_gl.balance
                dgl = credit_general_ledger_account(db=db, general_ledger_account_id=from_gl.id, amount=amount, commit=commit)
                if dgl['status'] == False:
                    return {
                        'status': False,
                        'message': dgl['message'],
                        'data': None
                    }
                else:
                    main_trans = create_transaction(db=db, country_id=country_id, currency_id=currency_id, gl_id=from_gl.id, type_id=transaction_type_id, action=TRANSACTION_ACTIONS['credit'], reference=reference, description=narration, narration=narration, amount=amount, previous_balance=dg_prev_balance, new_balance=dgl['data']['balance'], status=1, commit=commit)
                    from_done = True
            if from_acct is not None:
                da_prev_balance = from_acct.available_balance
                da = credit_account(db=db, account_id=from_acct.id, amount=amount, commit=commit)
                if da['status'] == False:
                    return {
                        'status': False,
                        'message': da['message'],
                        'data': None
                    }
                main_trans = create_transaction(db=db, country_id=country_id, currency_id=currency_id, user_id=from_acct.user_id, merchant_id=from_acct.merchant_id, account_id=from_acct.id, type_id=transaction_type_id, action=TRANSACTION_ACTIONS['credit'], reference=reference, description=narration, narration=narration, amount=amount, previous_balance=da_prev_balance, new_balance=da['data']['available_balance'], status=1, commit=commit)
                from_done = True
            if to_gl is not None:
                cgl_prvebalance = to_gl.balance
                cgl = debit_general_ledger_account(db=db, general_ledger_account_id=to_gl.id, amount=amount, commit=commit)
                if cgl['status'] == False:
                    return {
                        'status': False,
                        'message': cgl['message'],
                        'data': None
                    }
                create_transaction(db=db, country_id=country_id, currency_id=currency_id, gl_id=to_gl.id, type_id=transaction_type_id, action=TRANSACTION_ACTIONS['debit'], reference=reference, description=narration, narration=narration, amount=amount, previous_balance=cgl_prvebalance, new_balance=cgl['data']['balance'], status=1, commit=commit)
                to_done = True
            if to_acct is not None:
                ca_prev_balance = to_acct.available_balance
                ca = debit_account(db=db, account_id=to_acct.id, amount=amount, override=True, commit=commit)
                if ca['status'] == False:
                    return {
                        'status': False,
                        'message': ca['message'],
                        'data': None
                    }
                create_transaction(db=db, country_id=country_id, currency_id=currency_id, user_id=to_acct.user_id, merchant_id=to_acct.merchant_id, account_id=to_acct.id, type_id=transaction_type_id, action=TRANSACTION_ACTIONS['debit'], reference=reference, description=narration, narration=narration, amount=amount, previous_balance=ca_prev_balance, new_balance=ca['data']['available_balance'], status=1, commit=commit)
                to_done = True
    if from_done == False:
        return {
            'status': False,
            'message': str(from_account_number) + " not found",
            'data': None
        }
    else:
        if to_done == False:
            return {
                'status': False,
                'message': str(to_account_number) + " not found",
                'data': None
            }
        else:
            if main_trans is None:
                return {
                    'status': False,
                    'message': 'Unexpected transaction failure',
                    'data': None
                }
            else:
                return {
                    'status': True,
                    'message': 'Success',
                    'data': main_trans,
                }

def process_account_order(db: Session, user_id: int=0, country_id: int=0, merchant_id: int=0, amount: float=0, commit: bool=False):
    primary_account = get_single_user_primary_account(db=db, user_id=user_id)
    if primary_account is None:
        return {
            'status': False,
            'message': 'User does not have a primary account',
            'data': None
        }
    if primary_account.available_balance < amount:
        return {
            'status': False,
            'message': 'Insufficient balance',
            'data': None
        }
    merchant = get_single_merchant_by_id(db=db, id=merchant_id)
    currency = get_single_currency_by_code(db=db, code="NGN")
    currency_id = 0
    if merchant is not None:
        currency_id = merchant.currency_id
    if currency is not None:
        currency_id = currency.id
    order_suspense_account_number = None
    ors_config = get_single_system_configuration_by_name(db=db, name="order_suspense_account_number")
    if ors_config is not None:
        order_suspense_account_number = ors_config.single_value
    order_suspense_gl = get_single_general_ledger_account_by_account_number(db=db, account_number=order_suspense_account_number)
    if order_suspense_gl is None:
        return {
            'status': False,
            'message': 'Suspense not found',
            'data': None
        }
    order_trans_debit = get_single_transaction_type_by_code(db=db, code="029")
    # order_trans_credit = get_single_transaction_type_by_code(db=db, code="030")
    reference = generate_transaction_reference(tran_type=order_trans_debit.name)
    acct_prev_balance = primary_account.available_balance
    da = debit_account(db=db, account_id=primary_account.id, amount=amount, commit=commit)
    if da['status'] == False:
        return {
            'status': False,
            'message': da['message'],
            'data': None
        }
    main_trans = create_transaction(db=db, country_id=country_id, currency_id=currency_id, user_id=user_id, account_id=primary_account.id, type_id=order_trans_debit.id, action=TRANSACTION_ACTIONS['debit'], reference=reference, narration="New Order", amount=amount, previous_balance=acct_prev_balance, new_balance=da['data']['available_balance'], status=1, created_by=user_id, commit=commit)
    gl_prev_balance = order_suspense_gl.balance
    cgl = credit_general_ledger_account(db=db, general_ledger_account_id=order_suspense_gl.id, amount=amount, commit=commit)
    if cgl['status'] == False:
        return {
            'status': False,
            'message': cgl['message'],
            'data': None
        }
    create_transaction(db=db, country_id=country_id, currency_id=currency_id, gl_id=order_suspense_gl.id, type_id=order_trans_debit.id, action=TRANSACTION_ACTIONS['credit'], reference=reference, amount=amount, previous_balance=gl_prev_balance, new_balance=cgl['data']['balance'], status=1, commit=commit)
    return {
        'status': True,
        'message': 'Success',
        'data': main_trans
    }
