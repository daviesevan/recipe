# from flask import Blueprint, jsonify, request
# from sqlalchemy.orm import joinedload
# from app.admin.auth.routes import admin_required
# from app.models import Payment, db
# from app.admin.analytics.utils import (
#     get_total_user_count,
#     get_user_count_by_subscription,
#     get_verified_user_count,
#     get_active_user_count,
#     get_admin_count,
#     get_total_payments_by_subscription,
#     get_average_payment_amount,
#     get_payments_count_in_date_range,
#     get_users_below_search_threshold,
#     get_monthly_active_users,
#     get_yearly_revenue,
#     get_top_paying_users,
#     get_subscription_renewal_rate,
#     get_average_searches_per_user,
#     get_recipe_count,
#     get_total_payments_by_subscription,
#     get_transactions
# )
# from datetime import datetime, timedelta
# from functools import cache

# analyticsBp = Blueprint('analytics', __name__, url_prefix="/admin/analytics")

# @analyticsBp.get('/all')
# @admin_required
# def total_payments():
#     start_date = datetime.now().date() - timedelta(days=30)  # Last 30 days
#     end_date = datetime.now().date()
#     payments_count = get_payments_count_in_date_range(start_date, end_date)

#     total_admins = get_admin_count()
#     verified_users = get_verified_user_count()
#     # users_by_subscription = get_user_count_by_subscription()
#     total_users = get_total_user_count()
#     monthly_active_users = get_monthly_active_users()

#     return jsonify(verified_users=verified_users,
#                    total_admins=total_admins,
#                    total_users=total_users,
#                    payments_count=payments_count,
#                    monthly_active_users=monthly_active_users)

# @analyticsBp.get('/total-users')
# @admin_required
# def total_users():
#     total_users = get_total_user_count()
#     return jsonify(total_users=total_users)

# @analyticsBp.get('/users-by-subscription')
# @admin_required
# def users_by_subscription():
#     user_count_by_subscription = get_user_count_by_subscription()
#     return jsonify(users_by_subscription=user_count_by_subscription)

# @analyticsBp.get('/verified-users')
# @admin_required
# def verified_users():
#     verified_users = get_verified_user_count()
#     return jsonify(verified_users=verified_users)

# @analyticsBp.get('/active-users')
# @admin_required
# def active_users():
#     active_users = get_active_user_count()
#     return jsonify(active_users=active_users)

# @analyticsBp.get('/total-admins')
# @admin_required
# def total_admins():
#     total_admins = get_admin_count()
#     return jsonify(total_admins=total_admins)

# @analyticsBp.get('/payments-by-subscription')
# @admin_required
# def payments_by_subscription():
#     payments_by_subscription = get_total_payments_by_subscription()
#     return jsonify(payments_by_subscription=payments_by_subscription)

# @analyticsBp.get('/average-payment')
# @admin_required
# def average_payment():
#     average_payment = get_average_payment_amount()
#     return jsonify(average_payment=average_payment)

# @analyticsBp.get('/payments-in-range')
# @admin_required
# def payments_in_range():
#     start_date = datetime.now().date() - timedelta(days=30)  # Last 30 days
#     end_date = datetime.now().date()
#     payments_count = get_payments_count_in_date_range(start_date, end_date)
#     return jsonify(payments_count=payments_count)

# @analyticsBp.get('/users-below-threshold')
# @admin_required
# def users_below_threshold():
#     threshold = 10  # Example threshold
#     users_below_threshold = get_users_below_search_threshold(threshold)
#     return jsonify(users_below_threshold=users_below_threshold)

# @analyticsBp.get('/monthly-active-users')
# @admin_required
# def monthly_active_users():
#     monthly_active_users = get_monthly_active_users()
#     return jsonify(monthly_active_users=monthly_active_users)

# @analyticsBp.get('/yearly-revenue')
# @admin_required
# def yearly_revenue():
#     yearly_revenue = get_yearly_revenue()
#     return jsonify(yearly_revenue=yearly_revenue)

# @analyticsBp.get('/top-paying-users')
# @admin_required
# def top_paying_users():
#     limit = 10  # Example limit
#     top_paying_users = get_top_paying_users(limit)
#     return jsonify(top_paying_users=top_paying_users)

# @analyticsBp.get('/renewal-rate')
# @admin_required
# def renewal_rate():
#     renewal_rate = get_subscription_renewal_rate()
#     return jsonify(renewal_rate=renewal_rate)

# @analyticsBp.get('/average-searches')
# @admin_required
# def average_searches():
#     average_searches = get_average_searches_per_user()
#     return jsonify(average_searches=average_searches)

# @analyticsBp.get('/recipe-count')
# @admin_required
# def recipe_count():
#     recipe_count = get_recipe_count()
#     return jsonify(recipe_count=recipe_count)

# @analyticsBp.get('/transactions')
# @admin_required
# def recent_transactions():
#     page = request.args.get('page', 1, type=int)
#     per_page = request.args.get('per_page', 3, type=int)

#     transactions = Payment.query.options(joinedload(Payment.user)).order_by(Payment.payment_date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
#     response = {
#         'transactions': [{
#             'customer': payment.user.fullname,
#             'email': payment.user.email,
#             'type': 'Subscription' if payment.subscription_id else 'Sale',
#             'status': payment.payment_status,
#             'date': payment.payment_date.strftime('%Y-%m-%d'),
#             'amount': payment.amount,
#         } for payment in transactions.items],
#         'total_pages': transactions.pages,
#         'current_page': transactions.page
#     }
    
#     return jsonify(response)