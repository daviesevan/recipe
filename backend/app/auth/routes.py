import random
from flask import (Blueprint, 
                   jsonify, 
                   request)
from .utils import (hashPassword, 
                    verifyPassword, 
                    validateEmail)
from app.models import User, db, Subscription
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from flask_jwt_extended import (create_refresh_token, 
                                create_access_token, 
                                jwt_required, 
                                get_jwt_identity,
                                verify_jwt_in_request)
import resend
from datetime import datetime, timedelta
import os
from app.emails.notifications import send_email
from app.emails.reset_password_email import generate_password_reset_email
from functools import wraps

auth_bp = Blueprint("authentication", __name__, url_prefix="/auth")
resend.api_key = os.environ["RESEND_API_KEY"]


def get_default_subscription():
    # Get the 'free' subscription plan
    return Subscription.query.filter_by(plan='Free').first()

def user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Verify JWT token in the request headers
            verify_jwt_in_request()

            # Get the current user's identity from the JWT token
            current_user_id = get_jwt_identity()

            # Fetch the admin user from the database based on the current user's identity
            user = User.query.get(current_user_id)

            if not user:
                return jsonify(error='Unauthorized access'), 401

            # If user and authenticated, proceed with the wrapped function
            return func(*args, **kwargs)

        except Exception as e:
            return jsonify(error=f'Unauthorized access {e}'), 401


@auth_bp.post("/signup")
def signup():
    try:
        data = request.json
        fullname = data.get("fullname")
        email = data.get("email")
        password = data.get("password")

        if not fullname or not email or not password:
            return jsonify(error="All values are required"), 403
        
        if not validateEmail(email):
            return jsonify(error="Invalid Email. Try Again!"), 401
        
        if User.query.filter_by(email=email).first():
            return jsonify(error="Email already exists, Try Logging in!"), 401
        
        hashed_password = hashPassword(password)

        # Get the default 'free' subscription
        default_subscription = get_default_subscription()
        if not default_subscription:
            return jsonify(error="Default subscription plan not found"), 500
        
        newUser = User(
            email=email, 
            fullname=fullname, 
            password=hashed_password,
            subscription_id=default_subscription.id
        )
        db.session.add(newUser)
        db.session.commit()
        
        return jsonify(message=f"{fullname} created successfully"), 201

    except IntegrityError as e:
        db.session.rollback()
        print(f"IntegrityError: {e.orig}") 
        return jsonify(error='Database integrity error'), 500
        
    except UnmappedInstanceError as e:
        db.session.rollback()
        print(f"UnmappedInstanceError: {e}") 
        return jsonify(error='Invalid input data'), 400

    except Exception as e:
        db.session.rollback()
        print(f"Exception: {e}") 
        return jsonify(error='An error occurred'), 500

@auth_bp.post("/login")
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter(User.email == email).first()
        if not user:
            return jsonify(error="Email doesn't exist! Try logging in!"), 401
        if not verifyPassword(password, user.password):
            return jsonify(error="Wrong password. Please try again!"), 401
        
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify(
            access_token=access_token,
            refresh_token=refresh_token,
            message="Login successful!"
        ), 200

    except IntegrityError as e:
        db.session.rollback()
        return jsonify(error=f'An error occurred {e}'), 500

    except UnmappedInstanceError as e:
        db.session.rollback()
        return jsonify(error='Invalid input data'), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(error=f'An error occurred {e}'), 500

@auth_bp.post('/refresh')
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token), 200

@auth_bp.post('/forgot-password')
def forgot_password():
    try:
        data = request.json
        email = data.get("email")
        
        if not email:
            return jsonify(error="Email is required"), 400
        
        if not validateEmail(email):
            return jsonify(error="Invalid Email. Try Again!"), 401
        
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify(error="Email doesn't exist! Try signing up!"), 404
        
        reset_code = str(random.randint(100000, 999999))
        user.reset_token = reset_code
        user.reset_token_expiration = datetime.now() + timedelta(minutes=15)  # Token valid for 15 minutes
        db.session.commit()

        html_content = generate_password_reset_email(user, reset_code)
        response = send_email(user.email, "Your password reset code", html_content)
        return response
        
        # return jsonify(message="Password reset code sent to your email"), 200

    except IntegrityError as e:
        db.session.rollback()
        return jsonify(error=f'An error occurred {e}'), 500

    except UnmappedInstanceError as e:
        db.session.rollback()
        return jsonify(error='Invalid input data'), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(error=f'An error occurred {e}'), 500


@auth_bp.post('/reset-password')
def reset_password():
    try:
        data = request.json
        email = data.get("email")
        reset_code = data.get("reset_code")
        new_password = data.get("new_password")
        
        if not email or not reset_code or not new_password:
            return jsonify(error="All fields are required"), 400
        
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify(error="Invalid email or reset code"), 404

        if user.reset_token != reset_code:
            return jsonify(error="Invalid reset code"), 400
        
        if datetime.now() > user.reset_token_expiration:
            return jsonify(error="Reset code has expired"), 400
        
        hashed_password = hashPassword(new_password)
        user.password = hashed_password
        user.isEmailVerified = True
        user.reset_token = None  
        user.reset_token_expiration = None
        db.session.commit()
        
        return jsonify(message="Password has been reset successfully"), 200

    except IntegrityError as e:
        db.session.rollback()
        return jsonify(error=f'An error occurred {e}'), 500

    except UnmappedInstanceError as e:
        db.session.rollback()
        return jsonify(error='Invalid input data'), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(error=f'An error occurred {e}'), 500