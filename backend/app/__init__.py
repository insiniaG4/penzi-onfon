from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.extensions import db
from app.routes.sms_log import sms_log_bp
from app.routes.message import message_bp
from app.routes.match_routes import match_bp
from app.routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)

    # ✅ Enable CORS for all routes with explicit origin and methods
    CORS(app, resources={
        r"/users/*": {
            "origins": ["*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })

    @app.after_request
    def add_cors_headers(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response

    app.config.from_object(Config)
    db.init_app(app)

    # Register blueprints after CORS is initialized
    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix="/users")
    
    # Other blueprints...
    app.register_blueprint(sms_log_bp, url_prefix="/sms_log")
    app.register_blueprint(message_bp, url_prefix="/messages")
    app.register_blueprint(match_bp, url_prefix="/matches")

    with app.app_context():
        from app.models.message import Message
        db.create_all()

    return app


app = create_app()
