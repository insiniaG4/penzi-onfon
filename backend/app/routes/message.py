from flask import Blueprint, request, jsonify
from app.models.message import Message
from app.extensions import db

message_bp = Blueprint('messages', __name__)

@message_bp.route('/', methods=['POST'])
def send_message():
    data = request.get_json()

    # Validate required fields
    required = ['sender_phone', 'receiver_phone', 'message_text']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400

    message = Message(
        sender_phone=data['sender_phone'],
        receiver_phone=data['receiver_phone'],
        message_text=data['message_text'],
    )

    db.session.add(message)
    db.session.commit()

    return jsonify({'message': 'Sent successfully!'}), 201


@message_bp.route('/<string:phone_number>', methods=['GET'])
def get_messages(phone_number):
    messages = Message.query.filter(
        (Message.sender_phone == phone_number) |
        (Message.receiver_phone == phone_number)
    ).all()

    return jsonify([
        {
            'message_id': m.message_id,
            'sender_phone': m.sender_phone,
            'receiver_phone': m.receiver_phone,
            'message_text': m.message_text,
            'sent_at': m.sent_at.isoformat(),
            'status': m.status
        } for m in messages
    ]), 200
