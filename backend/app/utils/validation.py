from werkzeug.exceptions import BadRequest
import re
from datetime import datetime


class RegistrationValidator:
    """Comprehensive validation for registration steps"""
    
    # Valid options for dropdown fields
    VALID_GENDERS = ['male', 'female', 'other']
    VALID_COUNTIES = [
        'nairobi', 'mombasa', 'kisumu', 'nakuru', 'eldoret', 'thika', 'malindi',
        'kitale', 'garissa', 'kakamega', 'meru', 'nyeri', 'machakos', 'kericho',
        'embu', 'migori', 'homa_bay', 'turkana', 'west_pokot', 'samburu'
    ]
    VALID_EDUCATION_LEVELS = [
        'primary', 'secondary', 'certificate', 'diploma', 'bachelor', 'master', 'phd'
    ]
    VALID_MARITAL_STATUS = ['single', 'divorced', 'widowed', 'separated']
    VALID_RELIGIONS = [
        'christian', 'muslim', 'hindu', 'buddhist', 'traditional', 'other', 'none'
    ]
    VALID_ETHNICITIES = [
        'kikuyu', 'luhya', 'luo', 'kalenjin', 'kamba', 'kisii', 'meru', 'mijikenda',
        'turkana', 'maasai', 'somali', 'other'
    ]

    @staticmethod
    def validate_phone_number(phone_number):
        """Validate Kenyan phone number format"""
        if not phone_number:
            raise BadRequest("Phone number is required")
        
        # Remove spaces and special characters
        clean_phone = re.sub(r'[^\d+]', '', phone_number)
        
        # Kenyan phone number patterns
        patterns = [
            r'^\+254[17]\d{8}$',  # +254 format
            r'^254[17]\d{8}$',    # 254 format
            r'^0[17]\d{8}$'       # 0 format
        ]
        
        if not any(re.match(pattern, clean_phone) for pattern in patterns):
            raise BadRequest("Invalid Kenyan phone number format")
        
        return clean_phone

    @staticmethod
    def validate_username(username):
        """Validate username format and length"""
        if not username:
            raise BadRequest("Username is required")
        
        if len(username) < 3:
            raise BadRequest("Username must be at least 3 characters long")
        
        if len(username) > 50:
            raise BadRequest("Username must be less than 50 characters")
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise BadRequest("Username can only contain letters, numbers, and underscores")
        
        return username.lower()

    @staticmethod
    def validate_age(age):
        """Validate age range"""
        if not age:
            raise BadRequest("Age is required")
        
        try:
            age_int = int(age)
        except (ValueError, TypeError):
            raise BadRequest("Age must be a valid number")
        
        if age_int < 18:
            raise BadRequest("Must be at least 18 years old")
        
        if age_int > 100:
            raise BadRequest("Age must be less than 100")
        
        return age_int

    @staticmethod
    def validate_gender(gender):
        """Validate gender selection"""
        if not gender:
            raise BadRequest("Gender is required")
        
        gender_lower = gender.lower()
        if gender_lower not in RegistrationValidator.VALID_GENDERS:
            raise BadRequest(f"Invalid gender. Must be one of: {', '.join(RegistrationValidator.VALID_GENDERS)}")
        
        return gender_lower

    @staticmethod
    def validate_location(county, town):
        """Validate county and town"""
        if not county:
            raise BadRequest("County is required")
        
        if not town:
            raise BadRequest("Town is required")
        
        county_lower = county.lower()
        if county_lower not in RegistrationValidator.VALID_COUNTIES:
            raise BadRequest(f"Invalid county. Must be one of: {', '.join(RegistrationValidator.VALID_COUNTIES)}")
        
        if len(town) < 2:
            raise BadRequest("Town name must be at least 2 characters")
        
        if len(town) > 50:
            raise BadRequest("Town name must be less than 50 characters")
        
        return county_lower, town.title()

    @staticmethod
    def validate_education_level(education_level):
        """Validate education level"""
        if not education_level:
            raise BadRequest("Education level is required")
        
        education_lower = education_level.lower()
        if education_lower not in RegistrationValidator.VALID_EDUCATION_LEVELS:
            raise BadRequest(f"Invalid education level. Must be one of: {', '.join(RegistrationValidator.VALID_EDUCATION_LEVELS)}")
        
        return education_lower

    @staticmethod
    def validate_profession(profession):
        """Validate profession"""
        if not profession:
            raise BadRequest("Profession is required")
        
        if len(profession) < 2:
            raise BadRequest("Profession must be at least 2 characters")
        
        if len(profession) > 100:
            raise BadRequest("Profession must be less than 100 characters")
        
        return profession.title()

    @staticmethod
    def validate_marital_status(marital_status):
        """Validate marital status"""
        if not marital_status:
            raise BadRequest("Marital status is required")
        
        status_lower = marital_status.lower()
        if status_lower not in RegistrationValidator.VALID_MARITAL_STATUS:
            raise BadRequest(f"Invalid marital status. Must be one of: {', '.join(RegistrationValidator.VALID_MARITAL_STATUS)}")
        
        return status_lower

    @staticmethod
    def validate_religion(religion):
        """Validate religion"""
        if not religion:
            raise BadRequest("Religion is required")
        
        religion_lower = religion.lower()
        if religion_lower not in RegistrationValidator.VALID_RELIGIONS:
            raise BadRequest(f"Invalid religion. Must be one of: {', '.join(RegistrationValidator.VALID_RELIGIONS)}")
        
        return religion_lower

    @staticmethod
    def validate_ethnicity(ethnicity):
        """Validate ethnicity"""
        if not ethnicity:
            raise BadRequest("Ethnicity is required")
        
        ethnicity_lower = ethnicity.lower()
        if ethnicity_lower not in RegistrationValidator.VALID_ETHNICITIES:
            raise BadRequest(f"Invalid ethnicity. Must be one of: {', '.join(RegistrationValidator.VALID_ETHNICITIES)}")
        
        return ethnicity_lower

    @staticmethod
    def validate_self_description(self_description):
        """Validate self description"""
        if not self_description:
            raise BadRequest("Self description is required")
        
        if len(self_description) < 50:
            raise BadRequest("Self description must be at least 50 characters")
        
        if len(self_description) > 1000:
            raise BadRequest("Self description must be less than 1000 characters")
        
        # Check for inappropriate content (basic check)
        inappropriate_words = ['spam', 'scam', 'fake', 'money', 'cash', 'loan']
        description_lower = self_description.lower()
        
        for word in inappropriate_words:
            if word in description_lower:
                raise BadRequest("Self description contains inappropriate content")
        
        return self_description.strip()

    @staticmethod
    def validate_step_data(step_number, data):
        """Validate data for a specific registration step"""
        validated_data = {}
        
        if step_number == 1:  # Basic info
            validated_data['phone_number'] = RegistrationValidator.validate_phone_number(data.get('phone_number'))
            validated_data['username'] = RegistrationValidator.validate_username(data.get('username'))
            validated_data['age'] = RegistrationValidator.validate_age(data.get('age'))
            validated_data['gender'] = RegistrationValidator.validate_gender(data.get('gender'))
            
        elif step_number == 2:  # Location
            county, town = RegistrationValidator.validate_location(data.get('county'), data.get('town'))
            validated_data['county'] = county
            validated_data['town'] = town
            
        elif step_number == 3:  # Personal details
            validated_data['education_level'] = RegistrationValidator.validate_education_level(data.get('education_level'))
            validated_data['profession'] = RegistrationValidator.validate_profession(data.get('profession'))
            validated_data['marital_status'] = RegistrationValidator.validate_marital_status(data.get('marital_status'))
            
        elif step_number == 4:  # Cultural info
            validated_data['religion'] = RegistrationValidator.validate_religion(data.get('religion'))
            validated_data['ethnicity'] = RegistrationValidator.validate_ethnicity(data.get('ethnicity'))
            
        elif step_number == 5:  # Profile completion
            validated_data['self_description'] = RegistrationValidator.validate_self_description(data.get('self_description'))
        
        else:
            raise BadRequest("Invalid step number")
        
        return validated_data


# Legacy validation functions for backward compatibility
def validate_user_data(data, required_fields=None):
    if required_fields is None:
        required_fields = ['phone_number', 'username', 'age', 'gender', 'county', 'town']

    for field in required_fields:
        if field not in data:
            raise BadRequest(f"Missing required field: {field}")

def validate_match_data(data):
    if 'user_id' not in data or 'matched_user_id' not in data:
        raise BadRequest('Missing required fields: user_id, matched_user_id.')

def validate_message_data(data):
    required_fields = ['sender_id', 'receiver_id', 'message_text']
    for field in required_fields:
        if field not in data:
            raise BadRequest(f'Missing required field: {field}')