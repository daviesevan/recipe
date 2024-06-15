from flask_sqlalchemy import SQLAlchemy
from app.auth.utils import unique_id
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_id)
    email = db.Column(db.String(325), unique=True, nullable=False)
    fullname = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(325), nullable=False)
    isEmailVerified = db.Column(db.Boolean, default=False)
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiration = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id', name='fk_subscription_user'), nullable=False)
    searches_remaining = db.Column(db.Integer, default=10)

    subscription = db.relationship('Subscription', back_populates='users')
    payments = db.relationship('Payment', back_populates='user')

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_id)
    email = db.Column(db.String(325), unique=True, nullable=False)
    fullname = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(325), nullable=False)
    isEmailVerified = db.Column(db.Boolean, default=False)
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiration = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)

class Subscription(db.Model):
    __tablename__ = 'subscription'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_id)
    plan = db.Column(db.String(20), nullable=False)
    search_limit = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    users = db.relationship('User', back_populates='subscription')

class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, default=unique_id)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_payment_user'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.now)
    payment_status = db.Column(db.String(50), nullable=False)

    user = db.relationship('User', back_populates='payments')