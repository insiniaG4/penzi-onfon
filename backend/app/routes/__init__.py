from flask import Blueprint

from .user_routes import user_bp
from .match_routes import match_bp
from .message import message_bp
from .sms_log import sms_log_bp

def register_routes(app):
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(match_bp, url_prefix='/api/matches')
    app.register_blueprint(message_bp, url_prefix='/api/messages')
    app.register_blueprint(sms_log_bp, url_prefix='/api/sms-log')