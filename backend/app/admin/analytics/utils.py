from app.models import Payment, db, User, Subscription, Recipe, Admin
from sqlalchemy import func
from functools import cache
from datetime import datetime, timedelta

@cache
def get_total_user_count():
    return User.query.count()

# @cache
# def get_user_count_by_subscription():
#     return db.session.query(Subscription.plan, func.count(User.id)).join(User).group_by(Subscription.plan).all()

@cache
def get_verified_user_count():
    return User.query.filter(User.isEmailVerified == True).count()

@cache
def get_active_user_count(recent_days=30):
    cutoff_date = datetime.now() - timedelta(days=recent_days)
    return User.query.filter(User.updated_at >= cutoff_date).count()

@cache
def get_admin_count():
    return Admin.query.count()

@cache
def get_total_payments_by_subscription():
    return db.session.query(Subscription.plan, func.sum(Payment.amount)).join(Payment).group_by(Subscription.plan).all()

@cache
def get_average_payment_amount():
    return db.session.query(func.avg(Payment.amount)).filter(Payment.payment_status == "success").scalar() or 0

@cache
def get_payments_count_in_date_range(start_date, end_date):
    return Payment.query.filter(Payment.payment_date >= start_date, Payment.payment_date <= end_date).count()

@cache
def get_users_below_search_threshold(threshold=10):
    return User.query.filter(User.searches_remaining < threshold).count()

@cache
def get_monthly_active_users():
    current_month = datetime.now().month
    return User.query.filter(func.extract('month', User.updated_at) == current_month).count()

@cache
def get_yearly_revenue(year=None):
    if year is None:
        year = datetime.now().year
    return db.session.query(func.sum(Payment.amount)).filter(func.extract('year', Payment.payment_date) == year, Payment.payment_status == "success").scalar() or 0

@cache
def get_top_paying_users(limit=10):
    return db.session.query(User.email, func.sum(Payment.amount).label('total')).join(Payment).group_by(User.id).order_by(func.sum(Payment.amount).desc()).limit(limit).all()

@cache
def get_subscription_renewal_rate():
    total_subscriptions = db.session.query(Payment.user_id, func.count(Payment.id)).group_by(Payment.user_id).having(func.count(Payment.id) > 1).count()
    total_users = get_total_user_count()
    return (total_subscriptions / total_users) * 100 if total_users > 0 else 0

@cache
def get_average_searches_per_user():
    return db.session.query(func.avg(User.searches_remaining)).scalar() or 0

@cache
def get_recipe_count():
    return Recipe.query.count()
