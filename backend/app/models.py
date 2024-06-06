from flask_sqlalchemy import SQLAlchemy
from app.auth.utils import unique_id
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_id)
    email = db.Column(db.String(325), unique=True, nullable=False)
    fullname = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(325), nullable=False)
    isEmailVerified = db.Column(db.Boolean, default=False)
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiration = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
