from app.admin.auth.routes import admin_required
from flask import jsonify, Blueprint

dashboard_bp = Blueprint('admin', __name__, url_prefix='/admin/dashboard')

@dashboard_bp.route('/me')
@admin_required
def dashboard():
    # Only accessible by authenticated admins
    return jsonify(message='Welcome to the admin dashboard!')
