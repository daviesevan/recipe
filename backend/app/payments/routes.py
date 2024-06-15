from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Subscription, Payment, db

paymentBp = Blueprint('payments', __name__, url_prefix='/payment')

@paymentBp.post('/make')
@jwt_required()
def make_payment():
    data = request.json
    current_user = get_jwt_identity()

    subscription_id = data.get('subscription_id')
    user = User.query.get(current_user)
    subscription = Subscription.query.get(subscription_id)

    payment_amount = subscription.price
    payment_status = 'success'

    payment = Payment(
        user_id = user.id,
        amount = payment_amount,
        payment_status = payment_status
    )

    user.subscription = subscription.id
    user.searches_remaining = subscription.search_limit
    db.session.add(payment)
    db.session.commit()

    return jsonify({
        'message': 'Payment Successfull',
        'payment' : {
            'amount' : payment_amount,
            'payment_status' : payment.payment_status
        }
    }
    ), 201