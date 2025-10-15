from typing import Dict, List, Any
from sqlalchemy.orm import Session
from database.model import count_users, count_merchants, get_ids_of_general_ledger_account_types, get_ids_of_general_ledger_accounts, sum_of_transactions
from datetime import datetime, timedelta, timezone
import dateparser
from settings.constants import TRANSACTION_ACTIONS

def get_main_statistics(db: Session):
	total_registered_customers = 0
	on_time_delivery_rate = 0.0
	average_deliveries = 0.0
	late_deliveries = 0
	delivery_accuracy = 0.0
	wrong_deliveries = 0
	customer_ratings = 0.0
	compliants = 0
	deliveries_per_hour = 0.0
	delivery_success_rate = 0.0
	rider_availability = 0
	incident_reports = 0
	top_performers = 0
	low_performers = 0
	fast_moving_categories = 0
	slowest_moving_categories = 0
	top_selling_month = 0
	data = {
		"total_registered_customers": total_registered_customers,
		"on_time_delivery_rate": on_time_delivery_rate,
		"average_deliveries": average_deliveries,
		"late_deliveries": late_deliveries,
		"delivery_accuracy": delivery_accuracy,
		"wrong_deliveries": wrong_deliveries,
		"customer_ratings": customer_ratings,
		"compliants": compliants,
		"deliveries_per_hour": deliveries_per_hour,
		"rider_availability": rider_availability,
		"incident_reports": incident_reports,
		"top_performers": top_performers,
		"low_performers": low_performers,
		"fast_moving_categories": fast_moving_categories,
		"slowest_moving_categories": slowest_moving_categories,
		"top_selling_month": top_selling_month,
	}
	return {
		"status": True,
		"message": "Success",
		"data": data,
	}


def get_user_registration_stats(db: Session, timeline: str=None, days: int=None):
	today = datetime.today()
	from_day = None
	if timeline == "day":
		from_day = today - timedelta(days=1)
	elif timeline == "week":
		from_day = today - timedelta(days=7)
	elif timeline == "month":
		from_day = today - timedelta(days=30)
	elif timeline == "six_months":
		from_day = today - timedelta(days=180)
	elif timeline == "year":
		from_day = today - timedelta(days=365)
	if days is not None:
		if days > 0:
			from_day = today - timedelta(days=days)
	if from_day is None:
		return {
			"status": False,
			"message": "Invalid from days",
			"data": None
		}
	else:
		from_date = from_day.strftime("%Y-%m-%d %H:%M:%S")
		to_date = today.strftime("%Y-%m-%d %H:%M:%S")
		customers_count = count_users(db=db, filters={
			'user_type': 0,
			'from_date': from_date,
			'to_date': to_date,
		})
		merchants_count = count_merchants(db=db, filters={
			'from_date': from_date,
			'to_date': to_date,
		})
		data = {
			"customers_count": customers_count,
			"merchants_count": merchants_count,
		}
		return {
			"status": True,
			"message": "Success",
			"data": data
		}

def get_revenue_report_stats(db: Session, timeline: str=None, value_range: int=None):
	revenue_gl_type_ids = get_ids_of_general_ledger_account_types(db=db, filters={'type_number': 4})
	expense_gl_type_ids = get_ids_of_general_ledger_account_types(db=db, filters={'type_number': 5})
	revenue_gls = get_ids_of_general_ledger_accounts(db=db, filters={'type_ids': revenue_gl_type_ids})
	expense_gls = get_ids_of_general_ledger_accounts(db=db, filters={'type_ids': expense_gl_type_ids})
	now = datetime.now()
	data = []
	if timeline == "year":
		if value_range is None:
			value_range = 12
		elif value_range <= 0:
			value_range = 12
		for i in range(value_range):
			year = now.year - (1 if now.month - i <= 0 else 0)
			month = now.month - i if now.month - i > 0 else now.month - i + 12
			past = now.replace(year=year, month=month)
			first = past.replace(day=1)
			last = (past.replace(day=1, month=month+1 if month < 12 else 1, year=year+1 if month == 12 else year) - timedelta(days=1))
			day_value = past.strftime('%B %Y')
			first_day = first.strftime('%Y-%m-%d')
			first_day = dateparser.parse(first_day).astimezone(timezone.utc)
			last_day = last.strftime('%Y-%m-%d')
			last_day = dateparser.parse(last_day).astimezone(timezone.utc) + timedelta(days=1)
			revenue_sum = sum_of_transactions(db=db, filters={
				'gl_ids': revenue_gls,
				'action': TRANSACTION_ACTIONS['credit'],
				'from_date': first_day,
				'to_date': last_day,
			})
			if revenue_sum > 0:
				revenue_sum = round(revenue_sum, 2)
			expense_sum = sum_of_transactions(db=db, filters={
				'gl_ids': expense_gls,
				'action': TRANSACTION_ACTIONS['credit'],
				'from_date': first_day,
				'to_date': last_day,
			})
			if expense_sum > 0:
				expense_sum = round(expense_sum, 2)
			data.append({
				"month": day_value,
				"earning": revenue_sum,
				"expense": expense_sum,
			})
	if timeline == "month":
		if value_range is None:
			value_range = 4
		elif value_range <= 0:
			value_range = 4
		for i in range(value_range):
			week_start = first_day - timedelta(weeks=i)
			week_end = week_start + timedelta(days=6)
			first_day = week_start.strftime('%Y-%m-%d')
			last_day = week_end.strftime('%Y-%m-%d')
			first_day = first.strftime('%Y-%m-%d')
			first_day_par = dateparser.parse(first_day).astimezone(timezone.utc)
			last_day = last.strftime('%Y-%m-%d')
			last_day_par = dateparser.parse(last_day).astimezone(timezone.utc) + timedelta(days=1)
			day_value = f"{first_day} - {last_day}"
			revenue_sum = sum_of_transactions(db=db, filters={
				'gl_ids': revenue_gls,
				'action': TRANSACTION_ACTIONS['credit'],
				'from_date': first_day_par,
				'to_date': last_day_par,
			})
			if revenue_sum > 0:
				revenue_sum = round(revenue_sum, 2)
			expense_sum = sum_of_transactions(db=db, filters={
				'gl_ids': expense_gls,
				'action': TRANSACTION_ACTIONS['credit'],
				'from_date': first_day_par,
				'to_date': last_day_par,
			})
			if expense_sum > 0:
				expense_sum = round(expense_sum, 2)
			data.append({
				"month": day_value,
				"earning": revenue_sum,
				"expense": expense_sum,
			})
	if timeline == "week":
		if value_range is None:
			value_range = 7
		elif value_range <= 0:
			value_range = 7
		for i in range(value_range):
			day = now - timedelta(days=i)
			day_value = f"{day.strftime('%B %d, %Y')}"
			main_date = day.strftime('%Y-%m-%d')
			main_date_par = dateparser.parse(main_date).astimezone(timezone.utc)
			revenue_sum = sum_of_transactions(db=db, filters={
				'gl_ids': revenue_gls,
				'action': TRANSACTION_ACTIONS['credit'],
				'created_at': main_date_par,
			})
			if revenue_sum > 0:
				revenue_sum = round(revenue_sum, 2)
			expense_sum = sum_of_transactions(db=db, filters={
				'gl_ids': expense_gls,
				'action': TRANSACTION_ACTIONS['credit'],
				'created_at': main_date_par,
			})
			if expense_sum > 0:
				expense_sum = round(expense_sum, 2)
			data.append({
				"month": day_value,
				"earning": revenue_sum,
				"expense": expense_sum,
			})
	
	return {
		"status": True,
		"message": "Success",
		"data": data
	}

