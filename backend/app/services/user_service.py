from app.models import User
from app.extensions import db
from datetime import datetime

class UserService:
    @staticmethod
    def create_user(data):
        """Create a new user or return existing user if phone number exists"""
        # Check if user with this phone number already exists
        existing_user = UserService.get_user_by_phone(data['phone_number'])
        if existing_user:
            # User already exists, return the existing user
            return existing_user
            
        new_user = User(
            phone_number=data['phone_number'],
            username=data.get('username'),
            age=data.get('age'),
            gender=data.get('gender'),
            county=data.get('county'),
            town=data.get('town'),
            education_level=data.get('education_level'),
            profession=data.get('profession'),
            marital_status=data.get('marital_status'),
            religion=data.get('religion'),
            ethnicity=data.get('ethnicity'),
            self_description=data.get('self_description'),
            registration_status='complete' if UserService._is_complete_profile(data) else 'incomplete'
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def _is_complete_profile(data):
        """Check if profile data is complete"""
        required_fields = ['username', 'age', 'gender', 'county', 'town']
        return all(data.get(field) for field in required_fields)

    @staticmethod
    def get_user(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_phone(phone_number):
        """Get user by phone number"""
        return User.query.filter_by(phone_number=phone_number).first()

    @staticmethod
    def update_user(user_id, data):
        user = User.query.get(user_id)
        if user:
            # Update basic fields
            user.username = data.get('username', user.username)
            user.age = data.get('age', user.age)
            user.gender = data.get('gender', user.gender)
            user.county = data.get('county', user.county)
            user.town = data.get('town', user.town)
            user.education_level = data.get('education_level', user.education_level)
            user.profession = data.get('profession', user.profession)
            user.marital_status = data.get('marital_status', user.marital_status)
            user.religion = data.get('religion', user.religion)
            user.ethnicity = data.get('ethnicity', user.ethnicity)
            user.self_description = data.get('self_description', user.self_description)
            
            # Update registration status if provided
            if 'registration_status' in data:
                user.registration_status = data['registration_status']
            
            # Update timestamp
            user.updated_at = datetime.utcnow()
            
            # Check if profile is now complete
            if UserService._is_user_profile_complete(user):
                user.registration_status = 'Complete'
            
            db.session.commit()
            return user
        return None

    @staticmethod
    def _is_user_profile_complete(user):
        """Check if user profile is complete"""
        required_fields = ['username', 'age', 'gender', 'county', 'town', 'education_level', 'profession', 'marital_status', 'religion', 'ethnicity', 'self_description']
        return all(getattr(user, field) for field in required_fields)

    @staticmethod
    def get_complete_users():
        """Get all users with complete profiles"""
        return User.query.filter_by(registration_status='Complete').all()

    @staticmethod
    def get_incomplete_users():
        """Get all users with incomplete profiles"""
        return User.query.filter(User.registration_status != 'Complete').all()

    @staticmethod
    def search_users(criteria):
        """Search users based on criteria"""
        query = User.query.filter_by(registration_status='Complete')
        
        if criteria.get('age_min'):
            query = query.filter(User.age >= criteria['age_min'])
        if criteria.get('age_max'):
            query = query.filter(User.age <= criteria['age_max'])
        if criteria.get('gender'):
            query = query.filter(User.gender == criteria['gender'])
        if criteria.get('town'):
            query = query.filter(User.town == criteria['town'])
        if criteria.get('county'):
            query = query.filter(User.county == criteria['county'])
        if criteria.get('education_level'):
            query = query.filter(User.education_level == criteria['education_level'])
        if criteria.get('religion'):
            query = query.filter(User.religion == criteria['religion'])
        if criteria.get('marital_status'):
            query = query.filter(User.marital_status == criteria['marital_status'])
        
        return query.all()

    @staticmethod
    def get_user_stats():
        """Get user statistics"""
        total_users = User.query.count()
        complete_profiles = User.query.filter_by(registration_status='Complete').count()
        incomplete_profiles = total_users - complete_profiles
        
        return {
            'total_users': total_users,
            'complete_profiles': complete_profiles,
            'incomplete_profiles': incomplete_profiles,
            'completion_rate': (complete_profiles / total_users * 100) if total_users > 0 else 0
        }