from flask import Blueprint, request, jsonify
from app.models import Admin, db
from .utils import validateEmail, verifyPassword, hashPassword
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from app.emails.notifications import send_email
from app.emails.welcome_user_email import generate_welcome_email
from flask_jwt_extended import (create_access_token, 
                                create_refresh_token, 
                                get_jwt_identity, 
                                verify_jwt_in_request)
from functools import wraps


admin_bp = Blueprint('administration', __name__, url_prefix='/admin')

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Verify JWT token in the request headers
            verify_jwt_in_request()

            # Get the current user's identity from the JWT token
            current_user_id = get_jwt_identity()

            # Fetch the admin user from the database based on the current user's identity
            admin = Admin.query.get(current_user_id)

            if not admin:  # Adjust based on your Admin model
                return jsonify(error='Unauthorized access'), 401

            # If admin and authenticated, proceed with the wrapped function
            return func(*args, **kwargs)

        except Exception as e:
            return jsonify(error=f'Unauthorized access {e}'), 401

    return wrapper

@admin_bp.post('/signup')
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
        
        if Admin.query.filter_by(email=email).first():
            return jsonify(error="Email already exists, Try Logging in!"), 401
        
        hashed_password = hashPassword(password)
        newAdmin = Admin(email=email, fullname=fullname, password=hashed_password)
        db.session.add(newAdmin)
        db.session.commit()
        
        # Send welcome email to the newly created admin
        html_content = generate_welcome_email(fullname)
        response = send_email(email, "Welcome to our platform", html_content)
        return response
    
    except IntegrityError as e:
        db.session.rollback()
        if 'email' in str(e.orig):
            return jsonify(error='Email already exists'), 409
        
    except UnmappedInstanceError as e:
        db.session.rollback()
        return jsonify(error='Invalid input data'), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(error='An error occurred'), 500

@admin_bp.post('/login')
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify(error="Email and password are required"), 400
        
        admin = Admin.query.filter_by(email=email).first()
        if not admin or not verifyPassword(password, admin.password):
            return jsonify(error="Invalid credentials"), 401

        # Create JWT token for admin
        access_token = create_access_token(identity=admin.id)
        refresh_token = create_refresh_token(identity=admin.id)

        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    
    except Exception as e:
        return jsonify(error='An error occurred'), 500


