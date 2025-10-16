from typing import Dict
from sqlalchemy.orm import Session
from database.db import compare_laravel_datetime_with_today, get_added_laravel_datetime
from database.model import get_deposits_by_status, get_just_single_financial_product_by_id, debit_account_accrued, credit_account_accrued, get_just_single_account_by_id, get_single_general_ledger_account_by_id, debit_account, credit_account, create_transaction, debit_general_ledger_account, credit_general_ledger_account, update_deposit, get_single_account_type_by_id, get_single_transaction_type_by_code, update_account
from modules.utils.tools import get_current_date_formatted, get_current_date_laravel_formatted, generate_transaction_reference
from settings.constants import TRANSACTION_ACTIONS


def process_daily_deposits(db: Session):
	trans_debit = get_single_transaction_type_by_code(db=db, code="012")
	deposits = get_deposits_by_status(db=db, status=1)
	if len(deposits) > 0:
		for deposit in deposits:
			reference = generate_transaction_reference(tran_type=trans_debit.name)
			user_id = deposit.user_id
			merchant_id = deposit.matured_at
			deposit_account = get_just_single_account_by_id(db=db, id=deposit.account_id)
			if deposit_account is None:
				continue
			account_type = get_single_account_type_by_id(db=db, id=deposit.account_type_id)
			if account_type is None:
				continue
			financial_product = get_just_single_financial_product_by_id(db=db, id=account_type.product_id)
			if financial_product is None:
				continue
			country_id = financial_product.country_id
			currency_id = financial_product.currency_id
			interest_expense_gl = get_single_general_ledger_account_by_id(db=db, id=financial_product.interest_expense_gl_id)
			if interest_expense_gl is None:
				continue
			receiving_account_principal = get_just_single_account_by_id(db=db, id=deposit.receiving_account_principal_id)
			if receiving_account_principal is None:
				continue
			receiving_account_interest = get_just_single_account_by_id(db=db, id=deposit.receiving_account_interest_id)
			if receiving_account_interest is None:
				continue
			matured_at = deposit.matured_at
			if matured_at is None:
				matured_at = get_added_laravel_datetime(days=deposit.tenure)
			tenure = deposit.tenure
			rate = deposit.rate
			current_value = deposit.current_value
			amount = deposit.amount
			yield_amount = deposit.yield_amount
			comp_date = compare_laravel_datetime_with_today(datetime_str=matured_at)
			if comp_date == True:
				interest_amount = yield_amount - amount
        		interest_amount = round(interest_amount, 2)
				acct_prev_balance = deposit_account.available_balance
			    da = debit_account(db=db, account_id=deposit_account.id, amount=acct_prev_balance)
			    if da['status'] == False:
			        return {
			            'status': False,
			            'message': da['message'],
			            'data': None
			        }
			    create_transaction(db=db, country_id=country_id, currency_id=currency_id, user_id=user_id, merchant_id=merchant_id, account_id=deposit_account.id, type_id=trans_debit.id, deposit_id=deposit.id, action=TRANSACTION_ACTIONS['debit'], reference=reference, narration="Deposit Principal Liquidation", amount=acct_prev_balance, previous_balance=acct_prev_balance, new_balance=da['data']['available_balance'], status=1, created_by=user_id)
			    racct_prev_balance = receiving_account_principal.available_balance
			    ca = credit_account(db=db, account_id=receiving_account_principal.id, amount=acct_prev_balance)
			    if ca['status'] == False:
			        return {
			            'status': False,
			            'message': ca['message'],
			            'data': None
			        }
			    create_transaction(db=db, country_id=country_id, currency_id=currency_id, user_id=user_id, merchant_id=merchant_id, account_id=receiving_account_principal.id, type_id=trans_debit.id, deposit_id=deposit.id, action=TRANSACTION_ACTIONS['credit'], reference=reference, narration="Deposit Principal Liquidation", amount=acct_prev_balance, previous_balance=racct_prev_balance, new_balance=ca['data']['available_balance'], status=1, created_by=user_id)
			    if deposit_account.paid_interest_status == 0:
				    dprev_balance = interest_expense_gl.balance
			        dgl = debit_general_ledger_account(db=db, general_ledger_account_id=interest_expense_gl.id, amount=interest_amount)
			        if dgl['status'] == False:
			            return {
			                'status': False,
			                'message': dgl['message'],
			                'reference': None,
			            }
			        create_transaction(db=db, country_id=country_id, currency_id=currency_id, gl_id=interest_expense_gl.id, type_id=trans_debit.id, action=TRANSACTION_ACTIONS['debit'], reference=reference, narration="Deposit Interest Liquidation", amount=interest_amount, previous_balance=dprev_balance, new_balance=dgl['data']['balance'], status=1, created_by=user_id)
			        inacct_bal = receiving_account_interest.available_balance
			        ca = credit_account(db=db, account_id=receiving_account_interest.id, amount=interest_amount)
			        if ca['status'] == False:
			            return {
			                'status': False,
			                'message': ca['message'],
			                'data': None
			            }
			        create_transaction(db=db, country_id=country_id, currency_id=currency_id, user_id=user_id, merchant_id=merchant_id, account_id=receiving_account_interest.id, type_id=trans_debit.id, deposit_id=deposit.id, action=TRANSACTION_ACTIONS['credit'], reference=reference, narration="Deposit Interest Liquidation", amount=interest_amount, previous_balance=inacct_bal, new_balance=ca['data']['available_balance'], status=1, created_by=user_id)
				liquidated_at = get_current_date_laravel_formatted()
				update_deposit(db=db, id=deposit.id, values={'current_value': 0, 'status': 2, 'liquidated_at': liquidated_at})
				update_account(db=db, id=deposit_account.id, values={'accrued_balance': 0})
			else:
				interest_amount = (amount*rate*1) / (100*365)
				interest_amount = round(interest_amount, 2)
				current_value = current_value + interest_amount
				credit_account_accrued(db=db, account_id=deposit_account.id, amount=interest_amount)
				update_deposit(db=db, id=deposit.id, values={
					'current_value': current_value,
					'matured_at': matured_at,
					'status': 1,
				})
	return {
		'status': True,
		'message': 'Success',
	}