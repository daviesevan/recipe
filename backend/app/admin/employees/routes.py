from flask import Blueprint, jsonify
from app.admin.auth.routes import admin_required
from app.models import Admin, db

employee_bp = Blueprint('employees',
                        __name__, 
                        url_prefix='/employees')

@employee_bp.get('/')
@admin_required
def get_employees():
    employees = Admin.query.all()
    response = [{
        'id': emp.id,
        'email': emp.email,
        'fullname': emp.fullname,
        'isAdmin': emp.isAdmin,
        'created_at': emp.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for emp in employees]

    return jsonify(response)

@employee_bp.post('/<int:employee_id>/set_admin')
@admin_required
def set_admin(employee_id):
    employee = Admin.query.get(employee_id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    
    employee.isAdmin = True
    db.session.commit()
    
    return jsonify({'message': 'Admin rights granted'})

@employee_bp.post('/<int:employee_id>/revoke_admin')
@admin_required
def revoke_admin(employee_id):
    employee = Admin.query.get(employee_id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    
    employee.isAdmin = False
    db.session.commit()
    
    return jsonify({'message': 'Admin rights revoked'})