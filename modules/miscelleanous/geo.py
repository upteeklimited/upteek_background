from typing import Dict
from sqlalchemy.orm import Session
from database.model import get_countries, get_single_country_by_id, get_single_country_by_code, get_currencies, get_single_currency_by_id, get_single_currency_by_code, get_states, get_single_state_by_id, get_cities, get_single_city_by_id, get_lgas, get_single_lga_by_id
from fastapi_pagination.ext.sqlalchemy import paginate

def retrieve_countries(db: Session):
    countries = get_countries(db=db)
    return paginate(countries)

def retrieve_single_country(db: Session, id: int=0):
    country = get_single_country_by_id(db=db, id=id)
    if country is None:
        return {
            'status': False,
            'message': 'Country not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': country
        }
    
def retrieve_single_country_by_code(db: Session, code: str=None):
    country = get_single_country_by_code(db=db, code=code)
    if country is None:
        return {
            'status': False,
            'message': 'Country not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': country
        }
    
def retrieve_currencies(db: Session):
    currencies = get_currencies(db=db)
    return paginate(currencies)

def retrieve_single_currency(db: Session, currency_id: int=0):
    currency = get_single_currency_by_id(db=db, id=currency_id)
    if currency is None:
        return {
            'status': False,
            'message': 'Currency not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': currency
        }
    
def retrieve_single_currency_by_code(db: Session, code: str=None):
    currency = get_single_currency_by_code(db=db, code=code)
    if currency is None:
        return {
            'status': False,
            'message': 'Currency not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': currency
        }
    
def retrieve_states(db: Session, filters: Dict={}):
    states = get_states(db=db, filters=filters)
    return paginate(states)

def retrieve_single_state(db: Session, state_id: int=0):
    state = get_single_state_by_id(db=db, id=state_id)
    if state is None:
        return {
            'status': False,
            'message': 'State not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': state
        }

def retrieve_cities(db: Session, filters: Dict={}):
    cities = get_cities(db=db, filters=filters)
    return paginate(cities)

def retrieve_single_city(db: Session, city_id: int=0):
    city = get_single_city_by_id(db=db, id=city_id)
    if city is None:
        return {
            'status': False,
            'message': 'City not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': city
        }
    
def retrieve_lgas(db: Session, filters: Dict={}):
    lgas = get_lgas(db=db, filters=filters)
    return paginate(lgas)

def retrieve_single_lga(db: Session, lga_id: int=0):
    lga = get_single_lga_by_id(db=db, id=lga_id)
    if lga is None:
        return {
            'status': False,
            'message': 'LGA not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': lga
        }
