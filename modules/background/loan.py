from typing import Dict
from sqlalchemy.orm import Session
from database.model import filter_accounts, get_just_single_loan_by_id, get_just_single_account_by_id, get_single_general_ledger_account_by_id, create_transaction, debit_account, credit_account, debit_general_ledger_account, credit_general_ledger_account, update_transaction, get_collections, count_collection_loan_id_status, get_collections_by_collected_at, update_collection, get_single_user_primary_account, get_just_single_financial_product_by_id, get_just_single_loan_application_by_id, update_loan
from modules.utils.tools import get_current_date_alt_formatted, generate_transaction_reference
from settings.constants import TRANSACTION_ACTIONS

def process_end_of_day_collection(db: Session):
	collected_at = get_current_date_alt_formatted()
	collections = get_collections_by_collected_at(db=db, collected_at=collected_at)
	if len(collections):
		for collection in collections:
			if collection.status != 0:
				continue
			loan = get_just_single_loan_by_id(db=db, id=collection.loan_id)
			if loan is None:
				continue
			loan_application = get_just_single_loan_application_by_id(db=db, id=loan.application_id)
			if loan_application is None:
				continue
			financial_product = get_just_single_financial_product_by_id(db=db, id=loan_application.product_id)
			if financial_product is None:
				pass
			country_id = financial_product.country_id
			currency_id = financial_product.currency_id
			user_id = loan.user_id
			primary_account = get_single_user_primary_account(db=db, user_id=user_id)
			if primary_account is None:
				continue
			loan_account = get_just_single_account_by_id(db=db, id=loan.loan_account_id)
			if loan_account is None:
				continue
			income_gl = get_single_general_ledger_account_by_id(db=db, id=financial_product.interest_income_gl_id)
			if income_gl is None:
				continue
			loan_unpaid_principal = loan.unpaid_principal
			loan_unearned_interest = loan.unearned_interest
        	loan_status = loan.status
        	loan_is_paid = loan.is_paid
			bal_principal = collection.bal_principal
			bal_interest = collection.bal_interest
			bal_total = bal_principal + bal_interest
			bal_total = round(bal_total, 2)
			trans_debit = get_single_transaction_type_by_code(db=db, code="033")
			reference = generate_transaction_reference(tran_type=trans_debit.name)
			acct_prev_balance = primary_account.available_balance
		    da = debit_account(db=db, account_id=primary_account.id, amount=bal_total, override=True)
		    if da['status'] == False:
		        return {
		            'status': False,
		            'message': da['message'],
		            'data': None
		        }
		    main_trans = create_transaction(db=db, country_id=country_id, currency_id=currency_id, user_id=user_id, merchant_id=merchant_id, account_id=primary_account.id, collection_id=collection.id, loan_id=loan.id, type_id=trans_debit.id, action=TRANSACTION_ACTIONS['debit'], reference=reference, narration="Loan Payment", amount=bal_total, previous_balance=acct_prev_balance, new_balance=da['data']['available_balance'], status=1, created_by=user_id)
		    if bal_principal > 0:
		    	loan_acct_prev_balance = loan_account.available_balance
		        cla = credit_account(db=db, account_id=loan_account.id, amount=bal_principal)
		        if cla['status'] == False:
		            return {
		                'status': False,
		                'message': cla['message'],
		                'data': None
		            }
		        create_transaction(db=db, country_id=country_id, currency_id=currency_id, user_id=user_id, account_id=loan_account.id, collection_id=collection.id, loan_id=loan.id, type_id=trans_debit.id, action=TRANSACTION_ACTIONS['credit'], reference=reference, narration="Loan Payment Complete", amount=bal_principal, previous_balance=loan_acct_prev_balance, new_balance=cla['data']['available_balance'], status=1, created_by=user_id)
		        loan_unpaid_principal = loan_unpaid_principal - bal_principal
		    if bal_interest > 0:
		    	income_gl_prev_balance = income_gl.balance
		        cgl = credit_general_ledger_account(db=db, general_ledger_account_id=income_gl.id, amount=bal_interest)
		        if cgl['status'] == False:
		            return {
		                'status': False,
		                'message': cgl['message'],
		                'data': None
		            }
		        create_transaction(db=db, country_id=country_id, currency_id=currency_id, gl_id=income_gl.id, type_id=trans_debit.id, collection_id=collection.id, loan_id=loan.id, action=TRANSACTION_ACTIONS['credit'], reference=reference, amount=bal_interest, previous_balance=income_gl_prev_balance, new_balance=cgl['data']['balance'], status=1)
		        loan_unearned_interest = loan_unearned_interest - bal_interest
        	if loan_unpaid_principal <= 0:
        		loan_unpaid_principal = 0
        		loan_status = 1
        		loan_is_paid = 0
        	if loan_unearned_interest <= 0:
        		loan_unearned_interest = 0
        		loan_status = 2
        		loan_is_paid = 1
        	update_collection_by_loan_id(db=db, loan_id=loan.id, values={'bal_principal': 0, 'bal_interest': 0, 'status': 1})
        	update_loan(db=db, id=loan.id, values={'unpaid_principal': loan_unpaid_principal, 'unearned_interest': loan_unearned_interest, 'is_paid': loan_is_paid, 'status': loan_status})
	return {
		'status': True,
		'message': 'Success',
	}