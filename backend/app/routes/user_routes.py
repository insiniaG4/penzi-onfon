from flask import Blueprint, request, jsonify
from app.services import UserService
from app.utils import validate_user_data, format_response
from werkzeug.exceptions import BadRequest

user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['POST', 'OPTIONS'])
def register_user():
    if request.method == 'OPTIONS':
        return '', 204

    data = request.get_json()
    try:
        validate_user_data(data)
        user = UserService.create_user(data)
        return jsonify(format_response('User registered successfully!', {'user_id': user.id})), 201
    except BadRequest as e:
        return jsonify(format_response(str(e))), 400
    except Exception as e:
        return jsonify(format_response(str(e))), 500

@user_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = UserService.get_user(id)
    if user:
        return jsonify(format_response('User found', {
            'id': user.id,
            'phone_number': user.phone_number,
            'username': user.username,
            'age': user.age,
            'gender': user.gender,
            'county': user.county,
            'town': user.town,
            'education_level': user.education_level,
            'profession': user.profession,
            'marital_status': user.marital_status,
            'religion': user.religion,
            'ethnicity': user.ethnicity,
            'self_description': user.self_description,
            'registration_status': user.registration_status
        })), 200
    return jsonify(format_response('User not found')), 404

@user_bp.route('/phone/<phone_number>', methods=['GET'])
def get_user_by_phone(phone_number):
    user = UserService.get_user_by_phone(phone_number)
    if user:
        return jsonify(format_response('User found', {
            'id': user.id,
            'phone_number': user.phone_number,
            'username': user.username,
            'age': user.age,
            'gender': user.gender,
            'county': user.county,
            'town': user.town,
            'education_level': user.education_level,
            'profession': user.profession,
            'marital_status': user.marital_status,
            'religion': user.religion,
            'ethnicity': user.ethnicity,
            'self_description': user.self_description,
            'registration_status': user.registration_status
        })), 200
    return jsonify(format_response('User not found')), 404

@user_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    try:
        validate_user_data(data, required_fields=[])
        user = UserService.update_user(id, data)
        if user:
            return jsonify(format_response('User updated successfully!')), 200
        return jsonify(format_response('User not found')), 404
    except BadRequest as e:
        return jsonify(format_response(str(e))), 400
    except Exception as e:
        return jsonify(format_response(str(e))), 500

@user_bp.route('/matches', methods=['GET'])
def search_matches():
    try:
        criteria = {
            'age_min': request.args.get('age_min', type=int),
            'age_max': request.args.get('age_max', type=int),
            'town': request.args.get('town'),
            'gender': request.args.get('gender')
        }
        matches = UserService.search_users(criteria)
        return jsonify(format_response('Matches found', [
            {
                'id': user.id,
                'phone_number': user.phone_number,
                'username': user.username,
                'age': user.age,
                'gender': user.gender,
                'county': user.county,
                'town': user.town,
                'education_level': user.education_level,
                'profession': user.profession,
                'marital_status': user.marital_status,
                'religion': user.religion,
                'ethnicity': user.ethnicity,
                'self_description': user.self_description,
                'registration_status': user.registration_status
            } for user in matches
        ])), 200
    except Exception as e:
        return jsonify(format_response(str(e))), 500

@user_bp.route('/notify', methods=['POST'])
def notify_user():
    try:
        data = request.get_json()
        requester = data.get('requester')
        requested = data.get('requested')
        # Store notification in the database
        from app.models import Notification
        notification = Notification(
            requester_phone=requester['phone_number'],
            requested_phone=requested['phone_number']
        )
        db.session.add(notification)
        db.session.commit()
        return jsonify(format_response('Notification sent')), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(format_response(str(e))), 500

@user_bp.route('/requester/<phone_number>', methods=['GET'])
def get_requester(phone_number):
    try:
        from app.models import Notification, User
        notification = Notification.query.filter_by(requested_phone=phone_number).order_by(Notification.created_at.desc()).first()
        if notification:
            user = User.query.filter_by(phone_number=notification.requester_phone).first()
            if user:
                return jsonify(format_response('Requester found', {
                    'id': user.id,
                    'phone_number': user.phone_number,
                    'username': user.username,
                    'age': user.age,
                    'gender': user.gender,
                    'county': user.county,
                    'town': user.town,
                    'education_level': user.education_level,
                    'profession': user.profession,
                    'marital_status': user.marital_status,
                    'religion': user.religion,
                    'ethnicity': user.ethnicity,
                    'self_description': user.self_description,
                    'registration_status': user.registration_status
                })), 200
        return jsonify(format_response('No requester found')), 404
    except Exception as e:
        return jsonify(format_response(str(e))), 500