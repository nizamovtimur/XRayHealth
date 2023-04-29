import re


def validate(data, regex):
    return True if re.match(regex, data) else False


def validate_password(password: str):
    return validate(password, r'[A-Za-z0-9@#$%^&+=]{8,}')


def validate_email(email: str):
    return validate(email, r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')


def validate_analyze(**args):
    if not args.get('image_bytes') or not args.get('patient_id'):
        return {
            'image_bytes': 'Image is required',
            'patient_id': 'Patient ID is required'
        }
    if not isinstance(args.get('patient_id'), str):
        return {
            'patient_id': 'Patient ID must be a string'
        }
    if not isinstance(args.get('image_bytes'), bytes):
        return {
            'image_bytes': 'Image must be a bytes'
        }
    return True


def validate_user(**args):
    if not args.get('email') or not args.get('password') or not args.get('name'):
        return {
            'email': 'Email is required',
            'password': 'Password is required',
            'name': 'Name is required'
        }
    if not isinstance(args.get('name'), str) or \
            not isinstance(args.get('email'), str) or not isinstance(args.get('password'), str):
        return {
            'email': 'Email must be a string',
            'password': 'Password must be a string',
            'name': 'Name must be a string'
        }
    if not validate_email(args.get('email')):
        return {
            'email': 'Email is invalid'
        }
    if not validate_password(args.get('password')):
        return {
            'password': 'Password is invalid, should be at least 8 characters'
        }
    return True


def validate_email_and_password(email, password):
    if not (email and password):
        return {
            'email': 'Email is required',
            'password': 'Password is required'
        }
    if not validate_email(email):
        return {
            'email': 'Email is invalid'
        }
    if not validate_password(password):
        return {
            'password': 'Password is invalid, should be at least 8 characters'
        }
    return True
