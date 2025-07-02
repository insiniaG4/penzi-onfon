from app.extensions import db
from datetime import datetime

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requester_phone = db.Column(db.String(10), db.ForeignKey('user.phone_number'), nullable=False)
    requested_phone = db.Column(db.String(10), db.ForeignKey('user.phone_number'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)