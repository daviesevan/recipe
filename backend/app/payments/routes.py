from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Subscription, Payment, db
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
        subscription_id = data.get('subscription_id')
        is_annual = data.get('is_annual', False)

        if not subscription_id:
            return jsonify(
                error = "Subscription id is required"
            ), 400

        # Fetch the subscription details
        subscription = Subscription.query.get(subscription_id)
        if not subscription:
            return jsonify(error="Subscription not found"), 404

        # Get the current user's id
        user_identity = get_jwt_identity()
        user = User.query.filter_by(id=user_identity).first()
        if not user:
            return jsonify(error="User not found"), 404

        active_payment = Payment.query.filter(
            Payment.user_id == user.id,
            Payment.payment_deadline > datetime.now(),
            (Payment.payment_status == "completed") | (Payment.payment_status == "success")
        ).first()

        if active_payment:
            return jsonify(error="You already have an active subscription."), 400

        # Calculate the amount
        if is_annual:
            amount = int(subscription.price * 12 * 0.9 * 100)  # Annual price with 10% discount
            stored_amount = subscription.price * 12 * 0.9  # Annual price with discount
        else:
            amount = int(subscription.price * 100)  # Monthly price
            stored_amount = subscription.price  # Monthly price

        # Initialize payment with Paystack
        paystack_secret = os.environ['PAYSTACK_SECRET_KEY']
        headers = {
            "Authorization": f"Bearer {paystack_secret}",
            "Content-Type": "application/json"
        }
        payload = {
            "email": user.email,
            "customer_name":user.fullname,
            "amount": amount,
            "reference": unique_id(), 
            "callback_url": "https://s3gmmbpw-3000.uks1.devtunnels.ms/callback"
        }

        response = requests.post("https://api.paystack.co/transaction/initialize", json=payload, headers=headers)
        response_data = response.json()

        if response.status_code != 200:
            return jsonify(error="Failed to initialize payment"), 500

        payment = Payment(
            user_id=user.id,
            subscription_id=subscription.id,
            amount=stored_amount,
            payment_status="pending",
            reference=payload['reference'],
            payment_deadline=datetime.now() + timedelta(days=subscription.duration_days if not is_annual else subscription.duration_days * 12)
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
            payment = Payment.query.filter_by(user_id=user.id).order_by(Payment.payment_date.desc()).first()
            payment.payment_status = "completed"
            db.session.commit()

            print(f'{user.fullname}, {user.email}')

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
            payment = Payment.query.filter_by(reference=reference).first()

            if payment:
                payment.payment_status = 'success'
                payment.payment_date = datetime.now()

                user = payment.user
                subscription = payment.subscription

                user.searches_remaining = subscription.search_limit
                user.subscription_id = subscription.id
                user.subscription_deadline = datetime.now() + timedelta(days=subscription.duration_days)

                db.session.commit()

                return jsonify(status='success', message='Payment verified and user subscription updated'), 200

        return jsonify(status='failure', message='Invalid event or payment not found'), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(error=f"An error occurred: {str(e)}"), 500
