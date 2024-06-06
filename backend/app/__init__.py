from flask import Flask, Blueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import ApplicationConfiguration
from app.models import db
from flask_migrate import Migrate

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

    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    return app
