from typing import Dict
from sqlalchemy.orm import Session
from database.model import create_financial_product, FinancialProduct, create_general_ledger_account, get_single_general_ledger_account_type_by_account_code, get_last_general_ledger_account, update_financial_product, get_single_product_by_id, create_account_type, get_last_account_type, get_general_ledger_accounts, get_single_general_ledger_account_by_id, get_single_general_ledger_account_by_account_number
from modules.utils.acct import generate_internal_gl_number, generate_account_type_code

def create_gl(db: Session, account_type_code: str=None, account_name: str=None, created_by: int=0, authorized_by: int=0, commit: bool=False):
    last_gl = get_last_general_ledger_account(db=db)
    account_type = get_single_general_ledger_account_type_by_account_code(db=db, account_code=account_type_code)
    if account_type is None:
        return {
            'status': False,
            'message': 'Account type not found',
            'data': None
        }
    else:
        account_type_id = account_type.id
        account_number = generate_internal_gl_number(type_code=account_type_code, last_id=last_gl.id)
        gl = create_general_ledger_account(db=db, type_id=account_type_id, name=account_name, account_number=account_number, status=1, created_by=created_by, authorized_by=authorized_by, commit=commit)
        return {
            'status': True,
            'message': 'Success',
            'data': gl
        }

def create_product_gls(db: Session, product: FinancialProduct, created_by: int=0, authorized_by: int=0, commit: bool=False):
    product_type = product.product_type
    product_name = product.name
    reporting_gl_id = 0
    overdraft_gl_id = 0
    expense_gl_id = 0
    overdrawn_interest_gl_id = 0
    interest_receivable_gl_id = 0
    interest_payable_gl_id = 0
    income_gl_id = 0
    unearned_gl_id = 0
    fixed_gl_id = 0
    insurance_gl_id = 0
    last_gl_id = 0
    last_gl = get_last_general_ledger_account(db=db)
    if last_gl is not None:
        last_gl_id = last_gl.id
    asset_type_id = 0
    asset_account_code = "10000000"
    asset_type = get_single_general_ledger_account_type_by_account_code(db=db, account_code=asset_account_code)
    if asset_type is not None:
        asset_type_id = asset_type.id
    liability_account_code = "20000000"
    liability_type_id = 0
    liability_type = get_single_general_ledger_account_type_by_account_code(db=db, account_code=liability_account_code)
    if liability_type is not None:
        liability_type_id = liability_type.id
    income_account_code = "40000000"
    income_type_id = 0
    income_type = get_single_general_ledger_account_type_by_account_code(db=db, account_code=income_account_code)
    if income_type is not None:
        income_type_id = income_type.id
    expense_account_code = "50000000"
    expense_type_id = 0
    expense_type = get_single_general_ledger_account_type_by_account_code(db=db, account_code=expense_account_code)
    if expense_type is not None:
        expense_type_id = expense_type.id
    reporting_gl_name = product_name + " Reporting General Ledger "
    overdraft_gl_name = product_name + " Overdraft General Ledger "
    interest_expense_gl_name = product_name + "Interest Expense General Ledger "
    interest_income_gl_name = product_name + " Interest Income General Ledger "
    overdrawn_interest_income_gl_name = product_name + " Overdrawn Interest Income General Ledger "
    interest_receivable_gl_name = product_name + " Interest Receivable General Ledger "
    interest_payable_gl_name = product_name + " Interest Payable General Ledger "
    interest_unearned_gl_name = product_name + " Unearned Interest General Ledger "
    fixed_charge_gl_name = product_name + " Fixed Charge General Ledger "
    insurance_holding = product_name + " Insurance Holding "
    if product_type == 1:
        #savings        
        reporting_gl = create_general_ledger_account(db=db, type_id=liability_type_id, name=reporting_gl_name, account_number=generate_internal_gl_number(type_code=liability_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        reporting_gl_id = reporting_gl.id
        last_gl_id = reporting_gl_id

        overdraft_gl = create_general_ledger_account(db=db, type_id=asset_type_id, name=overdraft_gl_name, account_number=generate_internal_gl_number(type_code=asset_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        overdraft_gl_id = overdraft_gl.id
        last_gl_id = overdraft_gl_id

        expense_gl = create_general_ledger_account(db=db, type_id=expense_type_id, name=interest_expense_gl_name, account_number=generate_internal_gl_number(type_code=expense_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        expense_gl_id = expense_gl.id
        last_gl_id = expense_gl_id

        overdrawn_interest = create_general_ledger_account(db=db, type_id=income_type_id, name=overdrawn_interest_income_gl_name, account_number=generate_internal_gl_number(type_code=income_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        overdrawn_interest_gl_id = overdrawn_interest.id
        last_gl_id = overdrawn_interest_gl_id

        interest_receivable = create_general_ledger_account(db=db, type_id=asset_type_id, name=interest_receivable_gl_name, account_number=generate_internal_gl_number(type_code=asset_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        interest_receivable_gl_id = interest_receivable.id
        last_gl_id = interest_receivable_gl_id

        interest_payable = create_general_ledger_account(db=db, type_id=liability_type_id, name=interest_payable_gl_name, account_number=generate_internal_gl_number(type_code=liability_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        interest_payable_gl_id = interest_payable.id
        last_gl_id = interest_payable_gl_id
    elif product_type == 2:
        #current
        reporting_gl = create_general_ledger_account(db=db, type_id=liability_type_id, name=reporting_gl_name, account_number=generate_internal_gl_number(type_code=liability_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        reporting_gl_id = reporting_gl.id
        last_gl_id = reporting_gl_id

        overdraft_gl = create_general_ledger_account(db=db, type_id=asset_type_id, name=overdraft_gl_name, account_number=generate_internal_gl_number(type_code=asset_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        overdraft_gl_id = overdraft_gl.id
        last_gl_id = overdraft_gl_id

        expense_gl = create_general_ledger_account(db=db, type_id=expense_type_id, name=interest_expense_gl_name, account_number=generate_internal_gl_number(type_code=expense_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        expense_gl_id = expense_gl.id
        last_gl_id = expense_gl_id

        interest_income = create_general_ledger_account(db=db, type_id=income_type_id, name=interest_income_gl_name, account_number=generate_internal_gl_number(type_code=income_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        income_gl_id = interest_income.id
        last_gl_id = income_gl_id

        overdrawn_interest = create_general_ledger_account(db=db, type_id=income_type_id, name=overdrawn_interest_income_gl_name, account_number=generate_internal_gl_number(type_code=income_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        overdrawn_interest_gl_id = overdrawn_interest.id
        last_gl_id = overdrawn_interest_gl_id

        interest_receivable = create_general_ledger_account(db=db, type_id=asset_type_id, name=interest_receivable_gl_name, account_number=generate_internal_gl_number(type_code=asset_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        interest_receivable_gl_id = interest_receivable.id
        last_gl_id = interest_receivable_gl_id

        interest_payable = create_general_ledger_account(db=db, type_id=liability_type_id, name=interest_payable_gl_name, account_number=generate_internal_gl_number(type_code=liability_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        interest_payable_gl_id = interest_payable.id
        last_gl_id = interest_payable_gl_id
    elif product_type == 3:
        #deposit
        reporting_gl = create_general_ledger_account(db=db, type_id=liability_type_id, name=reporting_gl_name, account_number=generate_internal_gl_number(type_code=liability_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        reporting_gl_id = reporting_gl.id
        last_gl_id = reporting_gl_id

        expense_gl = create_general_ledger_account(db=db, type_id=expense_type_id, name=interest_expense_gl_name, account_number=generate_internal_gl_number(type_code=expense_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        expense_gl_id = expense_gl.id

        interest_payable = create_general_ledger_account(db=db, type_id=liability_type_id, name=interest_payable_gl_name, account_number=generate_internal_gl_number(type_code=liability_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by)
        interest_payable_gl_id = interest_payable.id
        last_gl_id = interest_payable_gl_id
        last_gl_id = expense_gl_id
    elif product_type == 4:
        #loan
        reporting_gl = create_general_ledger_account(db=db, type_id=liability_type_id, name=reporting_gl_name, account_number=generate_internal_gl_number(type_code=liability_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        reporting_gl_id = reporting_gl.id
        last_gl_id = reporting_gl_id

        expense_gl = create_general_ledger_account(db=db, type_id=expense_type_id, name=interest_expense_gl_name, account_number=generate_internal_gl_number(type_code=expense_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        expense_gl_id = expense_gl.id
        last_gl_id = expense_gl_id

        interest_income = create_general_ledger_account(db=db, type_id=income_type_id, name=interest_income_gl_name, account_number=generate_internal_gl_number(type_code=income_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        income_gl_id = interest_income.id
        last_gl_id = income_gl_id

        unearned_gl = create_general_ledger_account(db=db, type_id=expense_type_id, name=interest_unearned_gl_name, account_number=generate_internal_gl_number(type_code=expense_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        unearned_gl_id = unearned_gl.id
        last_gl_id = unearned_gl_id

        fixed_gl = create_general_ledger_account(db=db, type_id=income_type_id, name=fixed_charge_gl_name, account_number=generate_internal_gl_number(type_code=income_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        fixed_gl_id = fixed_gl.id
        last_gl_id = fixed_gl_id

        insurance_gl = create_general_ledger_account(db=db, type_id=income_type_id, name=insurance_holding, account_number=generate_internal_gl_number(type_code=income_account_code, last_id=last_gl_id), created_by=created_by, authorized_by=authorized_by, commit=commit)
        insurance_gl_id = insurance_gl.id
        last_gl_id = insurance_gl_id
    
    data = {
        'reporting_gl_id': reporting_gl_id,
        'overdraft_gl_id': overdraft_gl_id,
        'expense_gl_id': expense_gl_id,
        'overdrawn_interest_gl_id': overdrawn_interest_gl_id,
        'interest_receivable_gl_id': interest_receivable_gl_id,
        'interest_payable_gl_id': interest_payable_gl_id,
        'income_gl_id': income_gl_id,
        'unearned_gl_id': unearned_gl_id,
        'fixed_gl_id': fixed_gl_id,
        'insurance_gl_id': insurance_gl_id,
    }
    return {
        'status': True,
        'message': 'Success',
        'data': data
    }

def create_new_product(db: Session, name: str=None, description: str=None, product_type: int=0, created_by: int=0, authorized_by: int=0, commit: bool=False):
    interest_tenure_type = 0
    if product_type == 4:
        interest_tenure_type = 1
    product = create_financial_product(db=db, name=name, description=description, country_id=1, currency_id=1, product_type=product_type, interest_tenure_type=interest_tenure_type, user_type=1, status=1, created_by=created_by, authorized_by=authorized_by, commit=commit)
    resp = create_product_gls(db=db, product=product, created_by=created_by, authorized_by=authorized_by, commit=commit)
    resp_data = resp['data']
    values = {
        'gl_id': resp_data['reporting_gl_id'],
        'interest_expense_gl_id': resp_data['expense_gl_id'],
        'interest_income_gl_id': resp_data['income_gl_id'],
        'principal_unpaid_gl_id': resp_data['expense_gl_id'],
        'interest_unearned_gl_id': resp_data['unearned_gl_id'],
        'fixed_charge_gl_id': resp_data['fixed_gl_id'],
        'insurance_holding_gl_id': resp_data['insurance_gl_id'],
        'overdrawn_interest_gl_id': resp_data['overdrawn_interest_gl_id'],
        'liability_overdraft_gl_id': resp_data['overdraft_gl_id'],
        'interest_receivable_gl_id': resp_data['interest_receivable_gl_id'],
        'interest_payable_gl_id': resp_data['interest_payable_gl_id'],
    }
    update_financial_product(db=db, id=product.id, values=values, commit=commit)
    last_account_type_id = 0
    last_account_type = get_last_account_type(db=db)
    if last_account_type is not None:
        last_account_type_id = last_account_type.id
    account_type_code = generate_account_type_code(product_type=product_type, last_id=last_account_type_id)
    create_account_type(db=db, product_id=product.id, name=name, account_code=account_type_code, status=1, created_by=created_by, authorized_by=authorized_by, commit=commit)
    return {
        'status': True,
        'message': 'Success',
        'data': get_single_product_by_id(db=db, id=product.id)
    }

def retrieve_gls(db: Session, filters: Dict={}):
    data = get_general_ledger_accounts(db=db, filters=filters)
    return paginate(data)

def retrieve_single_gl(db: Session, gl_id: int=0):
    gl = get_single_general_ledger_account_by_id(db=db, id=gl_id)
    if gl is None:
        return {
            'status': False,
            'message': 'General Ledger not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': gl,
        }
    
def retrieve_single_gl_by_account_number(db: Session, account_number: str=None):
    gl = get_single_general_ledger_account_by_account_number(db=db, account_number=account_number)
    if gl is None:
        return {
            'status': False,
            'message': 'General Ledger not found',
            'data': None,
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': gl,
        }