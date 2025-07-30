from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc

from app.models import db, Message
from app.schemas import MessageSchema

blp = Blueprint("chat", __name__, description="Operations on chat")

# PUBLIC_INTERFACE
@blp.route("/chat")
class Chat(MethodView):
    """Send user message to chat and receive AI response."""
    @jwt_required()
    @blp.arguments(MessageSchema)
    @blp.response(201, MessageSchema)
    def post(self, message_data):
        user_id = get_jwt_identity()
        user_message = Message(
            user_id=user_id,
            text=message_data["text"],
            is_user=True
        )
        db.session.add(user_message)

        # Simulated AI response (replace with real AI model integration)
        ai_response_text = f"AI response to: {message_data['text']}"
        ai_message = Message(
            user_id=user_id,
            text=ai_response_text,
            is_user=False
        )
        db.session.add(ai_message)
        db.session.commit()
        return ai_message

# PUBLIC_INTERFACE
@blp.route("/chat/history")
class ChatHistory(MethodView):
    """Retrieve full chat history for authenticated user."""
    @jwt_required()
    @blp.response(200, MessageSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        messages = Message.query.filter_by(user_id=user_id).order_by(Message.timestamp.asc()).all()
        return messages
