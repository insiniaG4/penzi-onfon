from flask import jsonify

from app.models.user import User
from app.extensions import db


def handle_register(parsed):
    params = parsed.parameters
    phone = parsed.sender_phone

    existing_user = User.query.filter_by(phone_number=phone).first()
    if existing_user:
        return jsonify({"message": "Phone number already registered."}), 409

    new_user = User(
        phone_number=phone,
        username=params.get("name", "Anonymous"),
        age=params.get("age"),
        gender=params.get("gender"),
        county=params.get("county"),
        town=params.get("town")
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully."}), 201


def handle_match_request(parsed):
    # This is just a stub
    return jsonify({
        "message": "Match request received.",
        "params": parsed.parameters
    }), 200


def handle_message(parsed):
    return jsonify({
        "message": "Message command handled (to be implemented).",
        "params": parsed.parameters
    }), 200
