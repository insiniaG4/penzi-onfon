import re

def is_valid_phone_number(phone_number):
    pattern = r'^\+?[1-9]\d{1,14}$'
    return re.match(pattern, phone_number) is not None

def format_response(message, data=None):
    response = {'message': message}
    if data:
        response['data'] = data
    return response