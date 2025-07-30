from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class MessageSchema(Schema):
    id = fields.Int(dump_only=True)
    text = fields.Str(required=True)
    is_user = fields.Bool(required=True)
