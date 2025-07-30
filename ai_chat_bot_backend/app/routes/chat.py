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
    """
    Send user message to chat and receive AI response.

    The full user conversation history is retrieved from persistent storage (PostgreSQL)
    and used for context-aware AI replies. Both user messages and bot replies are
    stored in the database, allowing for contextually coherent responses.
    """
    @jwt_required()
    @blp.arguments(MessageSchema)
    @blp.response(201, MessageSchema)
    def post(self, message_data):
        """
        Send a user message and receive an AI bot reply.
        Stores both the user message and bot reply in persistent chat history.
        The AI reply is generated considering the user's full chat history for context.
        ---
        Request body: MessageSchema (text: str)
        Response: MessageSchema (AI chatbot reply)
        """
        user_id = get_jwt_identity()
        user_text = message_data["text"]

        # Store user message immediately for accurate sequential history
        user_message = Message(
            user_id=user_id,
            text=user_text,
            is_user=True
        )
        db.session.add(user_message)
        db.session.flush()  # Ensure user message is visible to query before commit

        # Retrieve all user conversation history (including this just-added message)
        chat_history = (
            Message.query
            .filter_by(user_id=user_id)
            .order_by(Message.timestamp.asc())
            .all()
        )

        # Format history for AI model: list of dicts [{role: ..., content: ...}]
        formatted_history = [
            {"role": "user" if msg.is_user else "assistant", "content": msg.text}
            for msg in chat_history
        ]

        # Generate AI response using conversation history as context
        # (This is a placeholder: replace with real model integration as needed)
        # Example: Echo last user input with indication of awareness of message count
        ai_response_text = (
            f"({len(formatted_history)} msg context) AI response to: "
            f"{user_text}"
            # Optionally show some context
            # f"\nConversation history: "
            # f"{' | '.join([m['content'] for m in formatted_history[-5:]])}"
        )

        # Persist AI bot reply
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
    """
    Retrieve full chat history for authenticated user.

    Returns an array of chat message objects (in chronological order).
    """
    @jwt_required()
    @blp.response(200, MessageSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        messages = Message.query.filter_by(user_id=user_id).order_by(Message.timestamp.asc()).all()
        return messages
