import logging
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, db
from app.auth.utils import hashPassword

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_settings_bp = Blueprint('user_settings', __name__, url_prefix="/user/settings")

@user_settings_bp.get('/')
@jwt_required()
def user_profile():
    try:
        current_user = get_jwt_identity()
        logger.info(f'Current user ID: {current_user}')
        
        user = User.query.filter_by(id=current_user).first()
        if user is None:
            logger.error(f'User with ID {current_user} not found')
            return jsonify(error="User not found"), 404
        
        return jsonify(
            email=user.email,
            password=user.password
        )
    except Exception as e:
        logger.exception(f'An error occurred while fetching the user profile: {e}')
        return jsonify(error="An internal error occurred"), 500

@user_settings_bp.put('/')
@jwt_required()
def update_user_profile():
    try:
        current_user = get_jwt_identity()
        logger.info(f'Current user ID: {current_user}')
        
        user = User.query.filter_by(id=current_user).first()
        if user is None:
            logger.error(f'User with ID {current_user} not found')
            return jsonify(error="User not found"), 404
        
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify(error="Email and password are required"), 400

        user.email = email
        user.password = hashPassword(password)
        
        db.session.commit()
        
        return jsonify(message="Profile updated successfully")
    except Exception as e:
        logger.exception(f'An error occurred while updating the user profile: {e}')
        return jsonify(error="An internal error occurred"), 500
