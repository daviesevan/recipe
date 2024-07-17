from flask import Blueprint, request, jsonify
from app.models import SubscriptionPlan, db
from flask_jwt_extended import jwt_required
# from datetime import datetime

subscription_bp = Blueprint('subscription', __name__, url_prefix='/admin/subscription')

@subscription_bp.post('/create')
@jwt_required()  
def create_subscription_plan():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    billing_cycle = data.get('billing_cycle')
    features = data.get('features')

    try:
        if not SubscriptionPlan.query.filter_by(name=name).first():
            new_plan = SubscriptionPlan(
                name=name,
                description=description,
                price=price,
                billing_cycle=billing_cycle,
                features=features
            )
            db.session.add(new_plan)
            db.session.commit()
            return jsonify(message=f"{name} subscription plan created successfully"), 201
        else:
            return jsonify(error=f"Subscription plan '{name}' already exists"), 400
    except Exception as e:
        db.session.rollback()
        print(f"Exception: {e}")
        return jsonify(error="An error occurred while creating the subscription plan"), 500

@subscription_bp.get('/')
@jwt_required()  
def get_subscription_plans():
    try:
        plans = SubscriptionPlan.query.all()
        plans_data = [
            {
                "id": plan.id,
                "name": plan.name,
                "description": plan.description,
                "price": plan.price,
                "billing_cycle": plan.billing_cycle,
                "features": plan.features
            } for plan in plans
        ]
        return jsonify(subscription_plans=plans_data), 200
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify(error="An error occurred while fetching subscription plans"), 500

@subscription_bp.put('/<int:plan_id>')
@jwt_required()
def update_subscription_plan(plan_id):
    data = request.json
    try:
        plan = SubscriptionPlan.query.get(plan_id)
        if not plan:
            return jsonify(error="Subscription plan not found"), 404

        plan.name = data.get('name', plan.name)
        plan.description = data.get('description', plan.description)
        plan.price = data.get('price', plan.price)
        plan.billing_cycle = data.get('billing_cycle', plan.billing_cycle)
        plan.features = data.get('features', plan.features)

        db.session.commit()
        return jsonify(message="Subscription plan updated successfully"), 200
    except Exception as e:
        db.session.rollback()
        print(f"Exception: {e}")
        return jsonify(error="An error occurred while updating the subscription plan"), 500

@subscription_bp.delete('/<int:plan_id>')
@jwt_required()
def delete_subscription_plan(plan_id):
    try:
        plan = SubscriptionPlan.query.get(plan_id)
        if not plan:
            return jsonify(error="Subscription plan not found"), 404

        db.session.delete(plan)
        db.session.commit()
        return jsonify(message="Subscription plan deleted successfully"), 200
    except Exception as e:
        db.session.rollback()
        print(f"Exception: {e}")
        return jsonify(error="An error occurred while deleting the subscription plan"), 500