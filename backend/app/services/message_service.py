from app.models.message import Message
from app.extensions import db

class MessageService:
    @staticmethod
    def send_message(sender_phone, receiver_phone, message_text):
        new_message = Message(
            sender_phone=sender_phone,
            receiver_phone=receiver_phone,
            message_text=message_text
        )
        db.session.add(new_message)
        db.session.commit()
        return new_message

    @staticmethod
    def get_messages(phone_number):
        return Message.query.filter(
            (Message.sender_phone == phone_number) |
            (Message.receiver_phone == phone_number)
        ).all()
