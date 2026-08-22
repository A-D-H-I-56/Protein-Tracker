import logging
import os
from flask import Flask
from app.config import config_by_name

def create_app(config_name: str = None) -> Flask:
    """
    Application Factory Pattern for Flask.
    Configures and initializes all blueprints, extensions, and logging.
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(
        __name__,
        static_folder=config_by_name[config_name].STATIC_FOLDER,
        template_folder=config_by_name[config_name].TEMPLATES_FOLDER
    )
    app.config.from_object(config_by_name[config_name])

    # Configure Logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s"
    )

    # Register Blueprints (Controller Layer)
    from app.controllers.web_controller import web_bp
    from app.controllers.api_controller import api_bp
    from app.controllers.error_controller import error_bp

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(error_bp)

    return app
