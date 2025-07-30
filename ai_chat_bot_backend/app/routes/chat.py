from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Message
from app.schemas import MessageSchema

blp = Blueprint("chat", __name__, description="Operations on chat")

@blp.route("/chat")
class Chat(MethodView):
    @jwt_required()
    @blp.arguments(MessageSchema)
    @blp.response(201, MessageSchema)
    def post(self, message_data):
        user_id = get_jwt_identity()
        
        # Save user message
        user_message = Message(
            user_id=user_id,
            text=message_data["text"],
            is_user=True
        )
        db.session.add(user_message)
        
        # AI response placeholder
        ai_response_text = f"AI response to: {message_data['text']}"
        ai_message = Message(
            user_id=user_id,
            text=ai_response_text,
            is_user=False
        )
        db.session.add(ai_message)
        db.session.commit()

        return ai_message

@blp.route("/chat/history")
class ChatHistory(MethodView):
    @jwt_required()
    @blp.response(200, MessageSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        messages = Message.query.filter_by(user_id=user_id).order_by(Message.id).all()
        return messages
