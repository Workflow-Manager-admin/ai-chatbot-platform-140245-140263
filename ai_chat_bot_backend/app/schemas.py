from marshmallow import Schema, fields

# PUBLIC_INTERFACE
class UserSchema(Schema):
    """User properties for public endpoints."""
    id = fields.Int(dump_only=True, metadata={"description": "User identifier"})
    username = fields.Str(required=True, metadata={"description": "Unique username"})
    password = fields.Str(required=True, load_only=True, metadata={"description": "Password (write only)"})
    email = fields.Str(load_only=True, required=False, metadata={"description": "User email"})

# PUBLIC_INTERFACE
class UserSignupSchema(Schema):
    """New user registration - requires username, password, and optional email."""
    username = fields.Str(required=True, metadata={"description": "New username"})
    password = fields.Str(required=True, metadata={"description": "Password"})
    email = fields.Str(required=False, metadata={"description": "Email for password recovery"})

# PUBLIC_INTERFACE
class UserLoginSchema(Schema):
    """User login fields."""
    username = fields.Str(required=True, metadata={"description": "Login username"})
    password = fields.Str(required=True, load_only=True, metadata={"description": "Password"})

# PUBLIC_INTERFACE
class PasswordResetRequestSchema(Schema):
    """Schema for initiating password reset (request token)."""
    email = fields.Str(required=True, metadata={"description": "Email for sending reset token"})

# PUBLIC_INTERFACE
class PasswordResetSchema(Schema):
    """Schema for resetting a password using provided token."""
    token = fields.Str(required=True, metadata={"description": "Password reset token"})
    password = fields.Str(required=True, metadata={"description": "New password"})

# PUBLIC_INTERFACE
class MessageSchema(Schema):
    """Chat message schema for create and retrieve."""
    id = fields.Int(dump_only=True, metadata={"description": "Message identifier"})
    text = fields.Str(required=True, metadata={"description": "Message content"})
    is_user = fields.Bool(required=True, metadata={"description": "Is message from user"})
    timestamp = fields.DateTime(dump_only=True, metadata={"description": "Timestamp"})
