from app.controllers.web_controller import web_bp
from app.controllers.api_controller import api_bp
from app.controllers.error_controller import error_bp

__all__ = [
    'web_bp',
    'api_bp',
    'error_bp'
]
