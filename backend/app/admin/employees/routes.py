from flask import Blueprint, jsonify, request
from app.admin.auth.routes import admin_required
from app.models import Admin, db

employee_bp = Blueprint('employees',
                        __name__, 
                        url_prefix='/employees')

@employee_bp.get('/')
@admin_required
def get_employees():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 3, type=int)
    
    employees_query = Admin.query.paginate(page=page, per_page=per_page)
    
    response = {
        'employees': [{
            'id': emp.id,
            'email': emp.email,
            'fullname': emp.fullname,
            'isAdmin': emp.isAdmin,
            'created_at': emp.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for emp in employees_query.items],
        'current_page': employees_query.page,
        'total_pages': employees_query.pages
    }

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