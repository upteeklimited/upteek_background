from typing import Dict, List, Any
from sqlalchemy.orm import Session
from database.model import get_users_by_user_type, get_single_system_configuration_by_name, get_single_user_by_id, get_single_user_primary_account, get_single_general_ledger_account_by_account_number, get_single_transaction_type_by_code, get_products_by_merchant_id, get_random_merchant_product, get_random_user_by_user_type
from modules.transactions.trans import create_general_posting
from modules.orders.post import create_new_order
from modules.authentication.auth import generate_new_user_account
from settings.constants import USER_TYPES

def fund_user(db: Session, user_id: int=0, amount: float=0, commit: bool=False):
	user = get_single_user_by_id(db=db, id=user_id)
	if user is None:
		return {
			'status': False,
			'message': 'User not found'
		}
	general_deposit_gl_config = get_single_system_configuration_by_name(db=db, name="general_deposit_gl")
	if general_deposit_gl_config is None:
		return {
			'status': False,
			'message': 'GL config not found',
		}
	general_deposit_gl = get_single_general_ledger_account_by_account_number(db=db, account_number=general_deposit_gl_config.single_value)
	if general_deposit_gl is None:
		return {
			'status': False,
			'message': 'GL not found',
		}
	primary_account = get_single_user_primary_account(db=db, user_id=user_id)
	if primary_account is None:
		return {
			'status': False,
			'message': 'Primary account not found',
		}
	trans_type = get_single_transaction_type_by_code(db=db, code="003")
	if trans_type is None:
		return {
			'status': False,
			'message': 'Transaction type not found',
		}
	return create_general_posting(db=db, transaction_type_id=trans_type.id, from_account_number=general_deposit_gl.account_number, to_account_number=primary_account.account_number, amount=amount, narration="Seed deposit", commit=commit)

def fund_all_seeded_customers(db: Session, amount: float=0, commit: bool=False):
	customer_users = get_users_by_user_type(db=db, user_type=USER_TYPES['customer']['num'])
	print(customer_users)
	if len(customer_users) > 0:
		for user in customer_users:
			print(user)
			print(fund_user(db=db, user_id=user.id, amount=amount, commit=commit))
	return True

def customer_users_random_purchase(db: Session, commit: bool=False):
	customer_users = get_users_by_user_type(db=db, user_type=USER_TYPES['customer']['num'])
	if len(customer_users) > 0:
		for user in customer_users:
			print(user)
			random_merchant = get_random_user_by_user_type(db=db, user_type=USER_TYPES['merchant']['num'])
			print(random_merchant)
			if random_merchant is not None:
				print(random_merchant.id)
				print(random_merchant.merchant_id)
				random_product = get_random_merchant_product(db=db, merchant_id=random_merchant.merchant_id)
				print(random_product)
				if random_product is not None:
					amount = random_product.price
					products = [{
					'product_id': random_product.id,
					'quantity': 1,
					'amount': amount,
					}]
					print(products)
					print(create_new_order(db=db, user_id=user.id, country_id=user.country_id, is_account=True, products=products, amount=amount, total_amount=amount, delivery_status=1, status=1, commit=commit))
	return True