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
    
    
    CORS(app, origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://52.48.121.185:8080", "http://52.48.121.185:8000"], supports_credentials=True)

    app.config.from_object(Config)
    db.init_app(app)

    
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(sms_log_bp, url_prefix="/sms_log")
    app.register_blueprint(message_bp, url_prefix="/messages")
    app.register_blueprint(match_bp, url_prefix="/matches")

    with app.app_context():
        from app.models.message import Message
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)