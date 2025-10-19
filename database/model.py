from typing import Dict
from sqlalchemy.orm import Session
from models.account_balances import Account_Balance, create_account_balance, update_account_balance, delete_account_balance, force_delete_account_balance, get_single_account_balance_by_id, get_account_balances
from models.account_types import AccountType, create_account_type, update_account_type, delete_account_type, force_delete_account_type, get_single_account_type_by_id, get_single_account_type_by_product_id, get_single_account_type_by_account_code, get_last_account_type, get_account_types
from models.accounts import Account, create_account, update_account, delete_account, force_delete_account, get_single_account_by_id, get_single_account_by_account_number, get_last_account, get_accounts, get_single_user_primary_account, search_accounts, filter_accounts, count_accounts, sum_of_account_balances
from models.activity_logs import Activity_Log, create_activity_log, update_activity_log, delete_activity_log, force_delete_activity_log, get_single_activity_log_by_id, get_activity_logs
from models.addresses import Address, create_address, update_address, delete_address, force_delete_address, get_single_address_by_id, get_addresses, get_addresses_by_addressable_type, get_addressable
from models.auth_tokens import AuthToken, create_auth_token, update_auth_token, update_user_auth_token, delete_auth_token, force_delete_auth_token, get_single_auth_token_by_id, get_auth_tokens, get_auth_tokens_by_user_id, get_latest_user_auth_token
from models.batch_logs import Batch_Log, create_batch_log, update_batch_log, delete_batch_log, force_delete_batch_log, get_single_batch_log_by_id, get_batch_logs
from models.batches import Batch, create_batch, update_batch, delete_batch, force_delete_batch, get_single_batch_by_id, get_batches
from models.beneficiaries import Beneficiary, create_beneficiary, update_beneficiary, delete_beneficiary, force_delete_beneficiary, get_single_beneficiary_by_id, get_beneficiaries
from models.bill_categories import BillCategory, create_bill_category, update_bill_category, delete_bill_category, force_delete_bill_category, get_single_bill_category_by_id, get_single_bill_category_by_code, get_bill_categories, count_bill_categories, count_bill_categories_by_code, check_bill_category_exist
from models.bills import Bill, create_bill, update_bill, delete_bill, force_delete_bill, get_single_bill_by_id, get_bills, count_bills, count_bills_by_code, check_if_bill_exists
from models.cards import Card, create_card, update_card, delete_card, force_delete_card, get_single_card_by_id, get_cards
from models.carts import Cart, create_cart, update_cart, delete_cart, force_delete_cart, get_single_cart_by_id, get_carts
from models.carts_products import CartProduct, create_cart_product, update_cart_product, delete_cart_product, force_delete_cart_product, get_all_carts_products
from models.categories import Category, create_category, update_category, delete_category, force_delete_category, get_single_category_by_id, get_single_category_by_slug, get_categories
from models.cities import City, create_city, update_city, delete_city, force_delete_city, get_single_city_by_id, get_capital_city, get_cities, get_cities_by_state_id
from models.collections import Collection, create_collection, update_collection, delete_collection, force_delete_collection, get_single_collection_by_id, get_collections
from models.compliance_usages import ComplianceUsage, create_compliance_usage, update_complaince_usage, delete_compliance_usage, force_delete_compliance_usage, get_single_complaince_usage_by_id, get_complaince_usages
from models.conversations import Conversation, create_conversation, update_conversation, delete_conversation, force_delete_conversation, get_single_conversation_by_id, get_all_conversations
from models.countries_currencies import CountryCurrency, create_country_currency, update_country_currency, delete_country_currency, force_delete_country_currency, get_single_country_currency_by_id, get_countries_currencies, get_countries_currencies_by_country_id, get_countries_currencies_by_currency_id
from models.countries import Country, create_country, update_country, delete_country, force_delete_country, get_single_country_by_id, get_single_country_by_code, get_countries
from models.currencies import Currency, create_currency, update_currency, delete_currency, force_delete_currency, get_single_currency_by_id, get_single_currency_by_code, get_currencies
from models.deposits import Deposit, create_deposit, update_deposit, delete_deposit, force_delete_deposit, get_single_deposit_by_id, get_deposits
from models.entities import Entity, create_entity, update_entity, delete_entity, force_delete_entity, get_single_entity_by_id, get_entities, get_people_by_entitiable_type, get_entitable
from models.favorites import Favorite, create_favorite, update_favorite, delete_favorite, force_delete_favorite, get_single_favorite_by_id, get_favorites, get_favorites_by_user_id_id_and_type
from models.financial_institutions import FinancialInstitution, create_financial_institution, update_financial_institution, delete_financial_institution, force_delete_financial_institution, get_single_financial_institution_by_id, get_financial_institutions
from models.financial_products import FinancialProduct, create_financial_product, update_financial_product, delete_financial_product, force_delete_financial_product, get_single_financial_product_by_id, get_financial_products
from models.general_ledger_account_types import GeneralLedgerAccountType, create_general_ledger_account_type, update_general_ledger_account_type, delete_general_ledger_account_type, force_delete_general_ledger_account_type, get_single_general_ledger_account_type_by_id, get_single_general_ledger_account_type_by_account_code, get_last_general_ledger_account_type, get_general_ledger_account_types, get_ids_of_general_ledger_account_types
from models.general_ledger_accounts import GeneralLedgerAccount, create_general_ledger_account, update_general_ledger_account, delete_general_ledger_account, force_delete_general_ledger_account, get_single_general_ledger_account_by_id, get_single_general_ledger_account_by_account_number, get_last_general_ledger_account, get_general_ledger_accounts, filter_general_ledger_accounts, search_general_ledger_accounts, get_ids_of_general_ledger_accounts
from models.groups_products import GroupProduct, create_group_product, update_group_product, delete_group_product, force_delete_group_product, get_single_group_product_by_id, get_groups_products
from models.groups import Group, create_group, update_group, delete_group, force_delete_group, get_single_group_by_id, get_single_group_by_slug, get_groups
from models.invoice_items import InvoiceItem, create_invoice_item, update_invoice_item, delete_invoice_item, force_delete_invoice_item, get_single_invoice_item_by_id, get_invoice_items
from models.invoice_requests import InvoiceRequest, create_invoice_request, update_invoice_request, delete_invoice_request, force_delete_invoice_request, get_single_invoice_request_by_id, get_invoice_requests
from models.invoices import Invoice, create_invoice, update_invoice, delete_invoice, force_delete_invoice, get_single_invoice_by_id, get_invoices
from models.jobs import Job, create_job, update_job, delete_job, force_delete_job, get_single_job_by_id, get_jobs
from models.l_g_a_s import LGA, create_lga, update_lga, delete_lga, force_delete_lga, get_single_lga_by_id, get_lgas, get_lgas_by_state_id
from models.loan_application_logs import LoanApplicationLog, create_loan_application_log, update_loan_application_log, delete_loan_application_log, force_delete_loan_application_log, get_single_loan_application_log_by_id, get_loan_application_logs
from models.loan_applications import LoanApplication, create_loan_application, update_loan_application, delete_loan_application, force_delete_loan_application, get_single_loan_application_by_id
from models.loans import Loan, create_loan, update_loan, delete_loan, force_delete_loan, get_single_loan_by_id, get_loans
from models.media_pivots import Medium_Pivot, create_medium_pivot, update_medium_pivot, delete_medium_pivot, force_delete_medium_pivot, get_medium_pivot, get_medium_pivot_by_medium_id, get_medium_pivot_by_mediumable_type_and_mediumable_id, get_medium_pivot_by_mediumable_type_and_mediumable_id_and_status, get_media_pivots
from models.media import Medium, create_medium, update_medium, delete_medium, force_delete_medium, get_single_medium_by_id, get_media, get_media_by_mediumable_type, get_mediumable
from models.merchant_categories import MerchantCategory, create_merchant_category, update_merchant_category, delete_merchant_category, force_delete_merchant_category, get_single_merchant_category_by_id, get_merchant_categories, get_merchant_categories_by_industry_id
from models.merchant_industries import MerchantIndustry, create_merchant_industry, update_merchant_industry, delete_merchant_industry, force_delete_merchant_industry, get_single_merchant_industry_by_id, get_merchant_industries
from models.merchants import Merchant, create_merchant, update_merchant, delete_merchant, force_delete_merchant, get_single_merchant_by_id, get_main_single_merchant_by_id, get_single_merchant_by_user_id, get_merchants, get_merchants_by_category_id, count_merchants
from models.merchants_users import Merchant_User, create_merchant_user, update_merchant_user, delete_merchant_user, force_delete_merchant_user, get_single_merchant_user_by_id, get_merchants_users
from models.messages import Message, create_message, update_message, delete_message, force_delete_message, get_all_messages
from models.notifications import Notification, create_notification, update_notification, delete_notification, force_delete_notification, get_all_notifications
from models.operators import Operator, create_operator, update_operator, delete_operator, force_delete_operator, get_single_operator_by_id, get_operators
from models.order_logs import OrderLog, create_order_log, update_order_log, delete_order_log, force_delete_order_log, get_single_order_log_by_id, get_order_logs
from models.orders_products import OrderProduct, create_order_product, update_order_product, delete_order_product, force_delete_order_product, get_all_orders_products
from models.orders import Order, create_order, update_order, delete_order, force_delete_order, get_single_order_by_id, get_orders, count_orders, sum_orders
from models.payment_links_products import PaymentLinkProduct, create_payment_link_product, update_payment_link_product, delete_payment_link_product, force_delete_payment_link_product, get_single_payment_link_product_by_id, get_payment_links_products
from models.payment_links import PaymentLink, create_payment_link, update_payment_link, delete_payment_link, force_delete_payment_link, get_single_payment_link_by_id, get_payment_links
from models.people import Person, create_person, update_person, delete_person, force_delete_person, get_single_person_by_id, get_people, get_people_by_personable_type, get_personable
from models.product_variants import ProductVariant, create_product_variant, update_product_variant, delete_product_variant, force_delete_product_variant, get_single_product_variant_by_id, get_product_variants
from models.products_categories import ProductCategory, create_product_category, update_product_category, delete_product_category, force_delete_product_category, get_all_products_categories
from models.products import Product, create_product, update_product, delete_product, force_delete_product, get_single_product_by_id, get_single_product_by_slug, get_products_by_merchant_id, get_products, count_products, count_products_by_merchant_id, get_random_merchant_product
from models.profiles import Profile, create_profile, update_profile, update_profile_by_user_id, delete_profile, force_delete_profile, get_single_profile_by_id, get_single_profile_by_user_id, count_profiles
from models.providers import Provider, create_provider, update_provider, delete_provider, force_delete_provider, get_single_provider_by_id, get_single_provider_by_code, check_provider_exist, get_providers
from models.reviews import Review, create_review, update_review, delete_review, force_delete_review, get_single_review_by_id, get_reviews
from models.scheduled_messages import ScheduledMessage, create_scheduled_message, update_scheduled_message, delete_scheduled_message, force_delete_scheduled_message, get_all_scheduled_messages
from models.services import Service, create_service, update_service, delete_service, force_delete_service, get_single_service_by_id, get_single_service_by_code, get_services, check_service_exist
from models.settings import Setting, create_setting, update_setting, update_setting_by_user_id, delete_setting, force_delete_setting, get_single_setting_by_id, get_single_setting_by_user_id
from models.statement_headers import Statement_Header, create_statement_header, update_statement_header, delete_statement_header, force_delete_statement_header, get_single_statement_header_by_id, get_statement_headers
from models.statements import Statement, create_statement, update_statement, delete_statement, force_delete_statement, get_single_statement_by_id, get_statements
from models.states import State, create_state, update_state, delete_state, force_delete_state, get_single_state_by_id, get_states, get_states_by_country_id
from models.sync_logs import SyncLog, create_sync_log, update_sync_log, update_sync_log_by_table_name, delete_sync_log, force_delete_sync_log, get_single_sycn_log_by_id, get_single_sycn_log_by_table_name, get_sync_logs
from models.system_configurations import SystemConfiguration, create_system_configuration, update_system_configuration, delete_system_configuration, force_delete_system_configuration, get_single_system_configuration_by_id, get_single_system_configuration_by_name, get_system_configurations
from models.tags_products import TagProduct, create_tag_product, update_tag_product, delete_tag_product, force_delete_tag_product, get_single_tag_product_by_id, get_tags_products
from models.tags import Tag, create_tag, update_tag, delete_tag, force_delete_tag, get_single_tag_by_id, get_single_tag_by_slug, get_tags
from models.tokens import Token, create_token, update_token, update_token_by_user_id, update_token_by_user_id_and_token_type, update_token_email, delete_token, force_delete_token, get_single_token_by_id, get_tokens, get_tokens_by_user_id, get_latest_user_token, get_latest_user_token_by_type, get_latest_user_token_by_type_and_status
from models.transaction_fees import TransactionFee, create_transaction_fee, update_transaction_fee, delete_transaction_fee, force_delete_transaction_fee, get_all_transaction_fees
from models.transaction_types import TransactionType, create_transaction_type, update_transaction_type, delete_transaction_type, force_delete_transaction_type, get_single_transaction_type_by_id, get_single_transaction_type_by_code, get_last_transaction_type, get_transaction_types
from models.transactions import Transaction, create_transaction, update_transaction, delete_transaction, force_delete_transaction, get_single_transaction_by_id, get_single_transaction_by_reference, get_single_transaction_by_external_reference, get_transactions, count_transactions, sum_of_transactions
from models.trial_balance_categories import Trial_Balance_Category, create_trial_balance_category, update_trial_balance_category, delete_trial_balance_category, force_delete_trial_balance_category, get_single_trial_balance_category_by_id, get_trial_balance_categories
from models.trial_balance_headers import Trial_Balance_Header, create_trial_balance_header, update_trial_balance_header, delete_trial_balance_header, force_delete_trial_balance_header, get_single_trial_balance_header_by_id, get_trial_balance_headers
from models.trial_balances import Trial_Balance, create_trial_balance, update_trial_balance, delete_trial_balance, force_delete_trial_balance, get_single_trial_balance_by_id, get_trial_balances
from models.user_device_logs import UserDeviceLog, create_user_device_log, update_user_device_log, delete_user_device_log, force_delete_user_device_log, get_single_user_device_log_by_id, get_user_devices_logs, get_user_device_logs_by_user_device_id
from models.user_devices import UserDevice, create_user_device, update_user_device, delete_user_device, force_delete_user_device, get_single_user_device_by_id, get_user_devices, get_user_devices_by_user_id
from models.users import User, create_user, update_user, delete_user, force_delete_user, get_single_user_by_id, get_main_single_user_by_id, get_single_user_by_email, get_single_user_by_email_and_user_type, get_single_user_by_phone_number, get_single_user_by_phone_number_and_user_type, get_single_searched_user_by_id, get_single_user_by_username, get_single_user_by_username_user_type, get_single_user_by_any_main_details, get_users, get_users_by_country_id, get_users_by_merchant_id, get_users_by_user_type, get_users_by_role, get_users_by_user_type_and_role, search_users, search_merchants_and_users, count_users, count_users_by_user_type, get_random_user_by_user_type
from models.virtual_accounts import VirtualAccount, create_virtual_account, update_virtual_account, delete_virtual_account, force_delete_virtual_account, get_single_virtual_account_by_id, get_virtual_accounts
from models.wallet_configurations import WalletConfiguration, create_wallet_configuration, update_wallet_configuration, delete_wallet_configuration, force_delete_wallet_configuration, get_single_wallet_configuration_by_id, get_single_wallet_configuration_by_user_id, get_single_wallet_configuration_by_merchant_id
import string
import random
from database.db import get_laravel_datetime
from modules.utils.auth import AuthHandler
from modules.utils.tools import generate_slug

auth = AuthHandler()

def id_generator(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_user_with_relevant_rows(db: Session, country_id: int = 0, currency_id: int = 0, merchant_id: int = 0, username: str = None, email: str = None, phone_number: str = None, password: str = None, device_token: str = None, external_provider: str = None, external_reference: str = None, user_type: int = 0, role: int = 0, first_name: str = None, other_name: str = None, last_name: str = None, date_of_birth: str = None, gender: str = None, bio: str = None, is_merchant: bool=False, merchant_name: str = None, merchant_trading_name: str = None, merchant_description: str = None, merchant_category_id: int = 0, merchant_currency_id: int = 0, merchant_phone_number: str = None, merchant_email: str = None, commit: bool=False):
    hashed_password = None
    if password is not None:
        hashed_password = auth.get_password_hash(password=password)
    user = create_user(db=db, country_id=country_id, username=username, email=email, phone_number=phone_number, password=hashed_password, device_token=device_token, external_provider=external_provider, external_reference=external_reference, user_type=user_type, role=role, status=1, commit=commit)
    create_profile(db=db, user_id=user.id, first_name=first_name, other_name=other_name, last_name=last_name, date_of_birth=date_of_birth, gender=gender, bio=bio, level_one_approved_by=1, level_one_approved_at=get_laravel_datetime(), commit=commit)
    create_setting(db=db, user_id=user.id, commit=commit)
    if is_merchant == True:
        slug = generate_slug(text=merchant_name)
        if merchant_currency_id > 0:
            currency_id = merchant_currency_id
        trading_name = None
        if merchant_trading_name is not None:
            trading_name = merchant_trading_name
        else:
            trading_name = merchant_name
        merchant = create_merchant(db=db, user_id=user.id, currency_id=currency_id, category_id=merchant_category_id, name=merchant_name, trading_name=trading_name, description=merchant_description, phone_number_one=merchant_phone_number, email=merchant_email, slug=slug, status=1, commit=commit)
        merchant_id = merchant.id
    if merchant_id > 0:
        update_user(db=db, id=user.id, values={'merchant_id': merchant_id})
    return user

def registration_unique_field_check(db: Session, phone_number: str=None, username: str=None, email: str=None, user_type: int=0):
    phone_number_check = get_single_user_by_phone_number_and_user_type(db=db, phone_number=phone_number, user_type=user_type)
    username_check = get_single_user_by_username_user_type(db=db, username=username, user_type=user_type)
    email_check = get_single_user_by_email_and_user_type(db=db, email=email, user_type=user_type)
    if phone_number_check is not None:
        return {
            'status': False,
            'message': 'Phone number already exist',
        }
    elif username_check is not None:
        return {
            'status': False,
            'message': 'Username already exist',
        }
    elif email_check is not None:
        return {
            'status': False,
            'message': 'Email already exist'
        }
    else:
        return {
            'status': True,
            'message': 'Validation successful'
        }

def debit_account(db: Session, account_id: int=0, amount: float=0, override: bool=False, commit: bool=False):
    account = get_single_account_by_id(db=db, id=account_id)
    if account is None:
        return {
            'status': False,
            'message': 'Account not found',
            'data': None,
        }
    if (account.available_balance < amount) and override == False:
        return {
            'status': False,
            'message': 'Insufficient balance',
            'data': None,
        }
    available_balance = account.available_balance - amount
    ledger_balance = account.ledger_balance - amount
    update_account(db=db, id=account_id, values={'available_balance': available_balance, 'ledger_balance': ledger_balance}, commit=commit)
    return {
        'status': True,
        'message': 'Account debited successfully',
        'data': {
            'available_balance': available_balance,
            'ledger_balance': ledger_balance
        }
    }

def credit_account(db: Session, account_id: int=0, amount: float=0, commit: bool=False):
    account = get_single_account_by_id(db=db, id=account_id)
    if account is None:
        return {
            'status': False,
            'message': 'Account not found',
            'data': None,
        }
    available_balance = account.available_balance + amount
    ledger_balance = account.ledger_balance + amount
    update_account(db=db, id=account_id, values={'available_balance': available_balance, 'ledger_balance': ledger_balance}, commit=commit)
    return {
        'status': True,
        'message': 'Account credited successfully',
        'data': {
            'available_balance': available_balance,
            'ledger_balance': ledger_balance
        }
    }

def debit_general_ledger_account(db: Session, general_ledger_account_id: int=0, amount: float=0, commit: bool=False):
    general_ledger_account = get_single_general_ledger_account_by_id(db=db, id=general_ledger_account_id)
    if general_ledger_account is None:
        return {
            'status': False,
            'message': 'General ledger account not found',
            'data': None,
        }
    balance = general_ledger_account.balance - amount
    update_general_ledger_account(db=db, id=general_ledger_account_id, values={'balance': balance}, commit=commit)
    return {
        'status': True,
        'message': 'General ledger account debited successfully',
        'data': {
            'balance': balance
        }
    }

def credit_general_ledger_account(db: Session, general_ledger_account_id: int=0, amount: float=0, commit: bool=False):
    general_ledger_account = get_single_general_ledger_account_by_id(db=db, id=general_ledger_account_id)
    if general_ledger_account is None:
        return {
            'status': False,
            'message': 'General ledger account not found',
            'data': None,
        }
    balance = general_ledger_account.balance + amount
    update_general_ledger_account(db=db, id=general_ledger_account_id, values={'balance': balance}, commit=commit)
    return {
        'status': True,
        'message': 'General ledger account credited successfully',
        'data': {
            'balance': balance
        }
    }
