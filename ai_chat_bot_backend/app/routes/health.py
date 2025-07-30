from flask_smorest import Blueprint
from flask.views import MethodView

blp = Blueprint("health", __name__, url_prefix="/", description="Health check endpoint for monitoring and liveness.")


# PUBLIC_INTERFACE
@blp.route("/")
class HealthCheck(MethodView):
    """
    Health check endpoint to verify service is running.
    """
    def get(self):
        return {"message": "Healthy"}
