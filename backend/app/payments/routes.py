from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, UserSubscription, PaymentTransaction, SubscriptionPlan, db
from app.auth.utils import unique_id
import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv, find_dotenv
from app.emails.notifications import send_email
from app.emails.payment_confirmation_email import generate_payment_confirmation_email

load_dotenv(find_dotenv())

paymentBp = Blueprint('payments', __name__, url_prefix='/payment')

@paymentBp.post('/initialize')
@jwt_required()
def initialize_payment():
    try:
        data = request.json
        plan_id = data.get('plan_id')
        is_annual = data.get('is_annual', False)

        if not plan_id:
            return jsonify(error="Subscription plan id is required"), 400

        # Fetch the subscription plan details
        plan = SubscriptionPlan.query.get(plan_id)
        if not plan:
            return jsonify(error="Subscription plan not found"), 404

        # Get the current user's id
        user_identity = get_jwt_identity()
        user = User.query.filter_by(id=user_identity).first()
        if not user:
            return jsonify(error="User not found"), 404

        active_subscription = UserSubscription.query.filter(
            UserSubscription.user_id == user.id,
            UserSubscription.end_date > datetime.now(),
            UserSubscription.status == "Active"
        ).first()

        if active_subscription:
            return jsonify(error="You already have an active subscription."), 400

        # Calculate the amount
        if is_annual:
            amount = int(plan.price * 12 * 0.9 * 100)  # Annual price with 10% discount
            stored_amount = plan.price * 12 * 0.9  # Annual price with discount
            end_date = datetime.now() + timedelta(days=365)
        else:
            amount = int(plan.price * 100)  # Monthly price
            stored_amount = plan.price  # Monthly price
            end_date = datetime.now() + timedelta(days=30)

        # Initialize payment with Paystack
        paystack_secret = os.environ['PAYSTACK_SECRET_KEY']
        headers = {
            "Authorization": f"Bearer {paystack_secret}",
            "Content-Type": "application/json"
        }
        payload = {
            "email": user.email,
            "amount": amount,
            "reference": unique_id(), 
            "callback_url": "https://s3gmmbpw-3000.uks1.devtunnels.ms/callback"
        }

        response = requests.post("https://api.paystack.co/transaction/initialize", json=payload, headers=headers)
        response_data = response.json()

        if response.status_code != 200:
            return jsonify(error="Failed to initialize payment"), 500

        # Create a new UserSubscription
        new_subscription = UserSubscription(
            user_id=user.id,
            plan_id=plan.id,
            start_date=datetime.now(),
            end_date=end_date,
            status="Pending",
            auto_renew=True
        )

        db.session.add(new_subscription)
        db.session.flush()  # This will assign an ID to new_subscription

        # Create a new PaymentTransaction
        payment = PaymentTransaction(
            user_id=user.id,
            subscription_id=new_subscription.id,
            amount=stored_amount,
            currency="KES",
            payment_method="Paystack",
            status="pending",
            transaction_date=datetime.now()
        )

        db.session.add(payment)
        db.session.commit()

        return jsonify(
            authorization_url=response_data['data']['authorization_url'],
            reference=payload['reference']
        ), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(error=f"An error occurred: {str(e)}"), 500

@paymentBp.post('/verify')
@jwt_required()
def verify_payment():
    try:
        data = request.json
        reference = data.get("reference")

        if not reference:
            return jsonify(error="Reference is required"), 400

        headers = {
            "Authorization": f"Bearer {os.environ['PAYSTACK_SECRET_KEY']}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"https://api.paystack.co/transaction/verify/{reference}", headers=headers)

        if response.status_code != 200:
            return jsonify(error="Payment verification failed"), response.status_code

        response_data = response.json()
        print(response_data)
        if response_data['data']['status'] == 'success':
            # Payment was successful, update payment record
            user_identity = get_jwt_identity()
            user = User.query.filter_by(id=user_identity).first()
            payment = PaymentTransaction.query.filter_by(user_id=user.id).order_by(PaymentTransaction.transaction_date.desc()).first()
            payment.status = "completed"
            
            # Update the corresponding UserSubscription
            subscription = UserSubscription.query.get(payment.subscription_id)
            subscription.status = "Active"
            
            db.session.commit()

            # Include payment details in the response
            payment_details = {
                "reference": response_data['data']['reference'],
                "status": response_data['data']['status'],
                "paid_at": response_data['data']['paid_at'],
                "channel": response_data['data']['channel'],
                "amount": response_data['data']['amount'],
                "currency": response_data['data']['currency'],
                "card_type": response_data['data']['authorization']['card_type'],
                "last4": response_data['data']['authorization']['last4'],
                "fees": response_data['data']['fees']
            }

            return jsonify(message="Payment verified successfully", user={
                "fullname": user.fullname,
                "email": user.email
            }, paymentDetails=payment_details), 200
        else:
            return jsonify(error="Payment was not successful"), 400

    except Exception as e:
        return jsonify(error=f"An error occurred: {str(e)}"), 500

@paymentBp.post('/webhook')
def webhook():
    try:
        data = request.json

        if data['event'] == 'charge.success':
            reference = data['data']['reference']
            payment = PaymentTransaction.query.filter_by(status="pending").order_by(PaymentTransaction.transaction_date.desc()).first()

            if payment:
                payment.status = 'success'
                
                user = payment.user
                subscription = UserSubscription.query.get(payment.subscription_id)
                subscription.status = "Active"

                # Update user's subscription details
                user.subscription_id = subscription.id

                db.session.commit()

                return jsonify(status='success', message='Payment verified and user subscription updated'), 200

        return jsonify(status='failure', message='Invalid event or payment not found'), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(error=f"An error occurred: {str(e)}"), 500