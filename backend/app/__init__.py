from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import ApplicationConfiguration
from app.models import db
from flask_migrate import Migrate
# from app.importrecipe import transfer_data

jwt = JWTManager()

def create_app():

    app = Flask(__name__)
    app.config.from_object(ApplicationConfiguration)

    jwt.init_app(app)
    db.init_app(app)
    CORS(app, supports_credentials=True)
    Migrate(app, db)

    # Register blue prints 
    from app.auth.routes import auth_bp
    from app.admin.subscriptions.routes import subscription_bp
    from app.admin.auth.routes import admin_bp
    from app.admin.dashboard.routes import dashboard_bp
    from app.payments.routes import paymentBp
    from app.admin.settings.routes import admin_settings_bp
    from app.admin.analytics.routes import analyticsBp
    from app.admin.employees.routes import employee_bp
    from app.settings.routes import user_settings_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(subscription_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(paymentBp)
    app.register_blueprint(admin_settings_bp)
    app.register_blueprint(analyticsBp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(user_settings_bp)

    with app.app_context():
        db.create_all()
        # transfer_data()

    return app
