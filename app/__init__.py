from flask import Flask
from .config import Config
from .extensions import db, migrate
from .api import api_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models
    from .routes import bp as todos_bp
    app.register_blueprint(todos_bp)
    app.register_blueprint(api_bp, url_prefix="/api/v1")
    # You may add severals blueprint when the app is bigger.
    return app