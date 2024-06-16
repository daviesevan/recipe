from flask import Blueprint, request, jsonify
from app.admin.auth.routes import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Admin, db
from app.admin.auth.utils import hashPassword
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

admin_settings_bp = Blueprint('admin_settings', __name__, url_prefix='/admin/settings')

@admin_settings_bp.post('/update/user')
@jwt_required()
@admin_required
def update_admin_settings():
    try:
        data = request.json
        new_email = data.get('email', None)
        new_password = data.get('password', None)
        setAdmin = data.get('set_admin', None)

        current_user = get_jwt_identity()
        admin = Admin.query.filter_by(id=current_user).first()
        if not admin:
            return jsonify(
                error="Admin doesn't exist in the company database!"
            ), 404
        
        if new_password:
            hashed_password = hashPassword(new_password)
            admin.password = hashed_password
            db.session.commit()
            return jsonify(message="Your password was updated successfully!"), 200

        if new_email:
            admin.email = new_email
            db.session.commit()
            return jsonify(message="Email updated successfully!"), 200
        
        if setAdmin:
            admin.isAdmin = setAdmin
            db.session.commit()
            return jsonify(message="Admin rights changed!"), 200
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify(error=f'An error occurred {e}'), 500

    except UnmappedInstanceError as e:
        db.session.rollback()
        return jsonify(error='Invalid input data'), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(error=f'An error occurred {e}'), 500
    
    return jsonify(error='An error occurred'), 500
    
