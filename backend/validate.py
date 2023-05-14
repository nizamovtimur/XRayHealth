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
            'image_bytes': 'Требуется изображение',
            'patient_id': 'Требуется ИД пациента'
        }
    if not isinstance(args.get('patient_id'), str):
        return {
            'patient_id': 'ИД пациента должен быть строкой'
        }
    if not isinstance(args.get('image_bytes'), bytes):
        return {
            'image_bytes': 'Требуется изображение'
        }
    return True


def validate_user(**args):
    if not args.get('email') or not args.get('password') or not args.get('name'):
        return {
            'email': 'Требуется Email',
            'password': 'Требуется пароль',
            'name': 'Требуется имя'
        }
    if not isinstance(args.get('name'), str) or \
            not isinstance(args.get('email'), str) or not isinstance(args.get('password'), str):
        return {
            'email': 'Email должен быть строкой',
            'password': 'Пароль должен быть строкой',
            'name': 'Имя должно быть строкой'
        }
    if not validate_email(args.get('email')):
        return {
            'email': 'Email не соответствует требованиям'
        }
    if not validate_password(args.get('password')):
        return {
            'password': 'Пароль должен содержать хотя бы 8 символов'
        }
    return True


def validate_email_and_password(email, password):
    if not (email and password):
        return {
            'email': 'Требуется Email',
            'password': 'Требуется пароль'
        }
    if not validate_email(email):
        return {
            'email': 'Требуется Email'
        }
    if not validate_password(password):
        return {
            'password': 'Пароль должен содержать хотя бы 8 символов'
        }
    return True
