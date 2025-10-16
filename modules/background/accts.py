from typing import Dict
from sqlalchemy.orm import Session
from database.model import create_account_balance, filter_accounts, get_general_ledger_accounts, get_single_account_type_by_id, get_single_financial_institution_by_id, debit_account_accrued, credit_account_accrued, get_single_account_type_by_product_id, get_financial_products
from modules.utils.tools import get_current_date_formatted


def store_todays_customers_balance(db: Session):
	current_date = get_current_date_formatted()
	accounts = filter_accounts(db=db)
	if len(accounts) > 0:
		for account in accounts:
			create_account_balance(db=db, account_id=account.id, balance=account.available_balance, ledger_balance=account.ledger_balance, account_status=account.status, is_eod=1, eod_date=current_date, status=1)
	return {
		'status': True,
		'message': 'Success',
	}

def store_todays_gls_balance(db: Session):
	current_date = get_current_date_formatted()
	gls = get_general_ledger_accounts(db=db)
	if len(gls) > 0:
		for gl in gls:
			balance = gl.balance
			positive_balance = 0
			negative_balance = 0
			if balance > 0:
				positive_balance = balance
			else:
				negative_balance = balance
			create_account_balance(db=db, gl_id=gl.id, balance=balance, gl_positive_balance=positive_balance, gl_negative_balance=negative_balance, account_status=gl.status, eod_date=current_date, status=1)
	return {
		'status': True,
		'message': 'Success'
	}

def process_daily_savings_account_accrual(db: Session):
	accounts_affected = 0
	products = get_financial_products(db=db, filters={'product_type': 1})
	if len(products) > 0:
		for product in products:
			interest_rate = product.interest_rate
			accounts = filter_accounts(db=db, filters={'product_id': product.id})
			if len(accounts) > 0:
				for account in accounts:
					balance = account.available_balance
					if balance > 0:
						interest = (balance*interest_rate*1) / (100*365)
						interest = round(interest, 2)
						credit_account_accrued(db=db, account_id=account.id, amount=interest)
						accounts_affected += 1
	return {
		'status': True,
		'message': 'Success: Account affected - ' + str(accounts_affected)
	}

def process_daily_current_account_accrual(db: Session):
	accounts_affected = 0
	products = get_financial_products(db=db, filters={'product_type': 2})
	if len(products) > 0:
		for product in products:
			interest_rate = product.interest_rate
			accounts = filter_accounts(db=db, filters={'product_id': product.id})
			if len(accounts) > 0:
				for account in accounts:
					balance = account.available_balance
					if balance > 0:
						interest = (balance*interest_rate*1) / (100*365)
						interest = round(interest, 2)
						credit_account_accrued(db=db, account_id=account.id, amount=interest)
						accounts_affected += 1
	return {
		'status': True,
		'message': 'Success: Account affected - ' + str(accounts_affected)
	}

