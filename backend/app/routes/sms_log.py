from flask import Blueprint, request, jsonify
from app.models.sms_log import SMSLog
from app.extensions import db
from app.utils.sms_parser import SMSParser
from app.services.sms_handlers import handle_match_request, handle_message, handle_register

sms_log_bp = Blueprint('sms_log', __name__)



@sms_log_bp.route('/', methods=['POST'])
def receive_sms():
    data = request.get_json()

    # Handle both 'sender'/'message' and 'from_number'/'message_content' formats
    sender_phone = data.get('sender') or data.get('from_number')
    message = data.get('message') or data.get('message_content')

    if not sender_phone or not message:
        return jsonify({'error': 'Missing sender phone number or message content'}), 400

    # Parse the SMS command
    parsed = SMSParser.parse_sms(message, sender_phone)

    # Log the SMS
    new_sms_log = SMSLog(
        from_number=sender_phone,
        to_number=data.get('to_number', 'PENZI'),
        message_type=data.get('message_type', 'INCOMING'),
        message_content=message
    )

    db.session.add(new_sms_log)
    db.session.commit()

    # Handle the parsed command
    try:
        if parsed.command == "REGISTER":
            response = handle_register(parsed)
        elif parsed.command == "MATCH":
            response = handle_match_request(parsed)
        elif parsed.command == "MESSAGE":
            response = handle_message(parsed)
        elif parsed.command == "HELP":
            response = jsonify({"message": SMSParser.get_help_text()})
        else:
            response = jsonify({
                "message": "SMS received and parsed successfully",
                "parsed_command": parsed.command,
                "parameters": parsed.parameters
            })
        
        return response
    except Exception as e:
        return jsonify({
            "error": "Error processing SMS command",
            "details": str(e),
            "parsed_command": parsed.command,
            "parameters": parsed.parameters
        }), 500

@sms_log_bp.route('/receive', methods=['POST'])
def receive_sms_alt():
    """Alternative endpoint for SMS reception"""
    return receive_sms()
