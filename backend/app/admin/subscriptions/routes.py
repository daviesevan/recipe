from flask import Blueprint, request, jsonify
from app.models import Subscription, db

subscription_bp = Blueprint('subscription', __name__, url_prefix='/admin/subscription')

@subscription_bp.post('/create')
def create_subscription():
    data = request.json
    plan = data.get('plan')
    price = data.get('price')
    search_limit = data.get('search_limit')

    try:
        if not Subscription.query.filter_by(plan=plan).first():
            new_subscription = Subscription(
                plan=plan,
                search_limit=search_limit,
                price=price
            )
        db.session.add(new_subscription)
        db.session.commit()
        return jsonify(message=f"{plan} subscriptions created successfully"), 201
    except Exception as e:
        db.session.rollback()
        print(f"Exception: {e}")
        return jsonify(error="An error occurred while creating dummy subscriptions"), 500