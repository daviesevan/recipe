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

    app.register_blueprint(auth_bp)
    app.register_blueprint(subscription_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(dashboard_bp)

    with app.app_context():
        # transfer_data()
        db.create_all()

    return app
