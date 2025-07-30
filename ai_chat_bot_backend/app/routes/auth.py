from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import request
import os
import datetime
import secrets

from app.models import db, User
from app.schemas import UserSchema, UserSignupSchema, UserLoginSchema, PasswordResetSchema, PasswordResetRequestSchema

blp = Blueprint("auth", __name__, description="User authentication and management APIs")

# PUBLIC_INTERFACE
@blp.route("/signup")
class UserSignup(MethodView):
    """Register a new user with secure password storage."""
    @blp.arguments(UserSignupSchema)
    @blp.response(201)
    def post(self, user_data):
        '''
        Register new user. Username must be unique. Email is optional.
        '''
        if User.query.filter_by(username=user_data["username"]).first():
            abort(409, message="A user with that username already exists.")
        if "email" in user_data and user_data["email"]:
            if User.query.filter_by(email=user_data["email"]).first():
                abort(409, message="A user with that email already exists.")
        user = User(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
            email=user_data.get("email", None)
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully."}, 201

# PUBLIC_INTERFACE
@blp.route("/login")
class UserLogin(MethodView):
    """Authenticate user and return JWT for session."""
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = User.query.filter_by(username=user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}
        abort(401, message="Invalid credentials.")

# PUBLIC_INTERFACE
@blp.route("/user")
class UserInfo(MethodView):
    """Retrieve info about the currently authenticated user."""
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        return user

# PUBLIC_INTERFACE
@blp.route("/password-reset/request")
class PasswordResetRequest(MethodView):
    """Request password reset: returns a reset token (simulates "send email")."""
    @blp.arguments(PasswordResetRequestSchema)
    def post(self, req_data):
        """
        Request a password reset for a user. Returns reset token (normally, would email this).
        """
        email = req_data.get("email")
        user = User.query.filter_by(email=email).first()
        if not user:
            abort(404, message="User with that email not found")

        # Simple random token (simulate real password reset mechanism)
        reset_token = secrets.token_urlsafe(32)
        expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        user.reset_token = reset_token
        user.reset_expiry = expiry
        db.session.commit()
        # In actual deployment, this should send an email, not return token directly!
        return {"reset_token": reset_token, "expires_at": expiry.isoformat()}, 200

# PUBLIC_INTERFACE
@blp.route("/password-reset/confirm")
class PasswordResetConfirm(MethodView):
    """Reset user password using a valid token."""
    @blp.arguments(PasswordResetSchema)
    def post(self, reset_data):
        """
        Reset the user's password using their reset token.
        """
        token = reset_data.get("token")
        password = reset_data.get("password")
        user = User.query.filter_by(reset_token=token).first()
        if not user or not user.reset_expiry or user.reset_expiry < datetime.datetime.utcnow():
            abort(401, message="Invalid or expired reset token")
        user.password = pbkdf2_sha256.hash(password)
        user.reset_token = None
        user.reset_expiry = None
        db.session.commit()
        return {"message": "Password reset successful"}
