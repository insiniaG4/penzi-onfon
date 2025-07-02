from app.extensions import db


class SMSLog(db.Model):
    __tablename__ = 'sms_log'
    
    id = db.Column(db.Integer, primary_key=True)
    from_number = db.Column(db.String(15))
    to_number = db.Column(db.String(15), nullable=False)
    message_type = db.Column(db.String(50), nullable=False)
    message_content = db.Column(db.Text, nullable=False)
    sent_date = db.Column(db.DateTime, default=db.func.now())
    
    def __repr__(self):
        return f'<SMSLog {self.id}: {self.from_number} -> {self.to_number}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'from_number': self.from_number,
            'to_number': self.to_number,
            'message_type': self.message_type,
            'message_content': self.message_content,
            'sent_date': self.sent_date.isoformat() if self.sent_date else None
        }