from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# PUBLIC_INTERFACE
class User(db.Model):
    """
    Database model for user accounts.
    Passwords are securely hashed before storage.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    # For password reset
    reset_token = db.Column(db.String(128), nullable=True)
    reset_expiry = db.Column(db.DateTime, nullable=True)

# PUBLIC_INTERFACE
class Message(db.Model):
    """
    Database model for chat messages, linked to user.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_user = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user = db.relationship('User', backref=db.backref('messages', lazy=True))
