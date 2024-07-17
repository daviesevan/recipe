from app.models import PaymentTransaction, db, User, UserSubscription, SubscriptionPlan, Recipe, Admin
from sqlalchemy import func
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload
from flask import request


def get_total_user_count():
    return User.query.count()

# 
# def get_user_count_by_subscription():
#     return db.session.query(Subscription.plan, func.count(User.id)).join(User).group_by(Subscription.plan).all()


def get_verified_user_count():
    return User.query.filter(User.isEmailVerified == True).count()  # noqa: E712


def get_active_user_count(recent_days=30):
    cutoff_date = datetime.now() - timedelta(days=recent_days)
    return User.query.filter(User.updated_at >= cutoff_date).count()


def get_admin_count():
    return Admin.query.count()

# 
# def get_total_payments_by_subscription():
#     return db.session.query(Subscription.plan, func.sum(Payment.amount)).join(Payment).group_by(Subscription.plan).all()


def get_average_payment_amount():
    return db.session.query(func.avg(PaymentTransaction.amount)).filter(PaymentTransaction.status == "success").scalar() or 0

def get_payments_count_in_date_range(start_date, end_date):
    return PaymentTransaction.query.filter(PaymentTransaction.transaction_date >= start_date, PaymentTransaction.transaction_date <= end_date).count()

def get_users_below_search_threshold(threshold=10):
    return User.query.filter(User.searches_remaining < threshold).count()


def get_monthly_active_users():
    current_month = datetime.now().month
    return User.query.filter(func.extract('month', User.updated_at) == current_month).count()


def get_yearly_revenue(year=None):
    if year is None:
        year = datetime.now().year
    return db.session.query(func.sum(PaymentTransaction.amount)).filter(
        func.extract('year', PaymentTransaction.transaction_date) == year,
        PaymentTransaction.status == "success"
    ).scalar() or 0

def get_top_paying_users(limit=10):
    return db.session.query(User.email, func.sum(PaymentTransaction.amount).label('total')).join(PaymentTransaction).group_by(User.id).order_by(func.sum(PaymentTransaction.amount).desc()).limit(limit).all()

def get_subscription_renewal_rate():
    total_subscriptions = db.session.query(UserSubscription.user_id).group_by(UserSubscription.user_id).having(func.count(UserSubscription.id) > 1).count()
    total_users = get_total_user_count()
    return (total_subscriptions / total_users) * 100 if total_users > 0 else 0


def get_average_searches_per_user():
    return db.session.query(func.avg(User.searches_remaining)).scalar() or 0


def get_recipe_count():
    return Recipe.query.count()


def get_total_payments_by_subscription():
    payments = db.session.query(PaymentTransaction).options(joinedload(PaymentTransaction.subscription)).all()
    payments_by_subscription = [
        {
            "id": payment.id,
            "user_id": payment.user_id,
            "subscription_id": payment.subscription_id,
            "amount": payment.amount,
            "transaction_date": payment.transaction_date.isoformat(),
            "status": payment.status,
            "payment_method": payment.payment_method,
            "subscription": {
                "id": payment.subscription.id,
                "plan_id": payment.subscription.plan_id,
                "start_date": payment.subscription.start_date.isoformat(),
                "end_date": payment.subscription.end_date.isoformat(),
                "status": payment.subscription.status,
                "auto_renew": payment.subscription.auto_renew
            }
        }
        for payment in payments
    ]
    return payments_by_subscription

def get_user_count_by_subscription():
    subscriptions = db.session.query(SubscriptionPlan).options(joinedload(SubscriptionPlan.user_subscriptions)).all()
    user_count_by_subscription = [
        {
            "subscription_id": subscription.id,
            "subscription_name": subscription.name,
            "user_count": len(subscription.user_subscriptions)
        }
        for subscription in subscriptions
    ]
    return user_count_by_subscription


def get_transactions():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    transactions = db.session.query(PaymentTransaction).options(joinedload(PaymentTransaction.user)).paginate(page, per_page, error_out=False)
    
    response = {
        'transactions': [{
            'customer': transaction.user.fullname,
            'email': transaction.user.email,
            'type': 'Subscription',
            'status': transaction.status,
            'date': transaction.transaction_date.strftime('%Y-%m-%d'),
            'amount': transaction.amount,
        } for transaction in transactions.items],
        'total_pages': transactions.pages,
        'current_page': transactions.page
    }
    
    return response