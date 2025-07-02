from flask import Blueprint, request, jsonify
from app.models import Match, User
from app.extensions import db
from sqlalchemy import and_

match_bp = Blueprint('matches', __name__)

# ✅ Create a new match
@match_bp.route('/', methods=['POST'])
def create_match():
    data = request.get_json()
    new_match = Match(
        user_id=data['user_id'],
        matched_user_id=data['matched_user_id']
    )
    db.session.add(new_match)
    db.session.commit()
    return jsonify({'message': 'Match created successfully!'}), 201

# ✅ Get matches by user ID
@match_bp.route('/<int:user_id>', methods=['GET'])
def get_matches(user_id):
    matches = Match.query.filter(
        (Match.user_id == user_id) | (Match.matched_user_id == user_id)
    ).all()
    return jsonify([{
        'id': match.id,
        'matched_user_id': match.matched_user_id,
        'status': match.status
    } for match in matches]), 200

# ✅ Search for matches using query params
@match_bp.route('/', methods=['GET'])
def search_matches():
    try:
        age_min = int(request.args.get('age_min', 18))
        age_max = int(request.args.get('age_max', 80))
        town = request.args.get('town', '').strip()
        gender = request.args.get('gender', '').strip().lower()

        query = User.query.filter(
            and_(
                User.age >= age_min,
                User.age <= age_max,
                User.gender.ilike(gender),
                User.town == town,
                User.registration_status == 'complete'
            )
        )

        results = query.all()
        return jsonify([
            {
                'username': u.username,
                'age': u.age,
                'town': u.town,
                'phone_number': u.phone_number,
                'education_level': u.education_level,
                'profession': u.profession,
                'marital_status': u.marital_status,
                'religion': u.religion,
                'ethnicity': u.ethnicity,
                'self_description': u.self_description
            } for u in results
        ]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ✅ Confirm a match (YES command)
@match_bp.route('/confirm', methods=['POST'])
def confirm_match():
    data = request.get_json()
    user = User.query.filter_by(phone_number=data['from_user']).first()
    match = User.query.filter_by(phone_number=data['to_user']).first()

    if user and match:
        existing = Match.query.filter_by(user_id=user.id, matched_user_id=match.id).first()
        if existing:
            existing.status = 'confirmed'
        else:
            new = Match(user_id=user.id, matched_user_id=match.id, status='confirmed')
            db.session.add(new)
        db.session.commit()
        return jsonify({'message': 'Match confirmed!'}), 200
    return jsonify({'message': 'User(s) not found'}), 404

# ✅ Decline a match (NO command)
@match_bp.route('/decline', methods=['POST'])
def decline_match():
    data = request.get_json()
    user = User.query.filter_by(phone_number=data['from_user']).first()
    match = User.query.filter_by(phone_number=data['to_user']).first()

    if user and match:
        existing = Match.query.filter_by(user_id=user.id, matched_user_id=match.id).first()
        if existing:
            existing.status = 'declined'
        else:
            new = Match(user_id=user.id, matched_user_id=match.id, status='declined')
            db.session.add(new)
        db.session.commit()
        return jsonify({'message': 'Match declined!'}), 200
    return jsonify({'message': 'User(s) not found'}), 404
