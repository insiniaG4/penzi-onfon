from app.extensions import db

class Message(db.Model):
    __tablename__ = 'incoming_messages'

    message_id = db.Column(db.Integer, primary_key=True)
    sender_phone = db.Column(db.String(15), nullable=False)
    receiver_phone = db.Column(db.String(15), nullable=False)
    message_text = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=db.func.now())
    status = db.Column(db.String(20), nullable=False, default='sent')

    def __repr__(self):
        return f"<Message {self.sender_phone} → {self.receiver_phone}>"
