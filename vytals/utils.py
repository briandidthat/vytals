from datetime import date, datetime
from functools import wraps

from cerberus import Validator
from email_validator import validate_email, EmailNotValidError
from flask import jsonify
from flask_jwt_extended import get_jwt_claims, verify_jwt_in_request

from vytals.exceptions import InvalidUsage

to_date = lambda s: datetime.strptime(s, '%Y-%m-%d')
to_date_time = lambda s: datetime.fromisoformat(s)


def test_email_address(email: str):
    try:
        valid = validate_email(email)
        return str(valid.email)
    except EmailNotValidError as e:
        raise InvalidUsage(message=str(e), status_code=422)


def calculate_duration(start_time: datetime, end_time: datetime):
    if not all(isinstance(i, datetime) for i in [start_time, end_time]):
        raise InvalidUsage(message="Invalid type.", status_code=422)

    difference = end_time - start_time
    seconds = difference.total_seconds()
    minutes = divmod(seconds, 60)

    return minutes


# will calculate age based on current date - birthdate
def calculate_age(birth_date: date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    return age


# will parse user data from json and return User instance
def parse_user(JSON: dict):
    first_name = JSON.get('first_name', None)
    last_name = JSON.get('last_name', None)
    username = JSON.get('username', None)
    password = JSON.get('password', None)
    birthdate_string = JSON.get('birthdate', None)
    birthdate = date.fromisoformat(birthdate_string)
    email = JSON.get('email', None)

    from vytals.models import User
    return User(first_name, last_name, username, password, email, birthdate)


# will parse reading data from json and return Reading instance
def parse_reading(JSON: dict):
    weight = JSON.get('weight', None)
    blood_pressure = JSON.get('blood_pressure', None)
    temperature = JSON.get('temperature', None)
    oxygen_level = JSON.get('oxygen_level', None)
    pulse = JSON.get('pulse', None)
    date_time = JSON.get('date_time', None)
    timestamp = datetime.fromisoformat(date_time)  # convert string to datetime object

    from vytals.models import Reading
    return Reading(weight, blood_pressure, temperature, oxygen_level, pulse, timestamp, None)


# will parse activity data from json and return Activity instance
def parse_activity(JSON: dict):
    type = JSON.get('type', None)
    description = JSON.get('description', None)
    start_time = JSON.get('start_time', None)
    end_time = JSON.get('end_time', None)
    start_datetime = datetime.fromisoformat(start_time)  # convert string to datetime object
    end_datetime = datetime.fromisoformat(end_time)  # convert string to datetime object
    user_id = JSON.get('user_id', None)

    from vytals.models import Activity
    return Activity(type, description, start_datetime, end_datetime, user_id)


login_schema = {
    'username': {
        'type': 'string'
    },
    'password': {
        'type': 'string'
    }
}

login_validator = Validator(login_schema)

user_schema = {
    'first_name': {
        'type': 'string'
    },
    'last_name': {
        'type': 'string'
    },
    'username': {
        'type': 'string'
    },
    'password': {
        'type': 'string'
    },
    'birthdate': {
        'type': 'date',
        'coerce': to_date
    },
    'email': {
        'type': 'string',
        'coerce': test_email_address,
    }
}

user_validator = Validator(user_schema)

reading_schema = {
    'weight': {
        'type': 'number'
    },
    'blood_pressure': {
        'type': 'number'
    },
    'temperature': {
        'type': 'number'
    },
    'oxygen_level': {
        'type': 'number'
    },
    'pulse': {
        'type': 'number'
    },
    'date_time': {
        'type': 'datetime',
        'coerce': to_date_time
    }
}

reading_validator = Validator(reading_schema)

activity_schema = {
    'type': {
        'type': 'string'
    },
    'description': {
        'type': 'string'
    },
    'start_time': {
        'type': 'datetime',
        'coerce': to_date_time
    },
    'end_time': {
        'type': 'datetime',
        'coerce': to_date_time
    }
}

activity_validator = Validator(activity_schema)


# custom decorator to verify the jwt token and check for appropriate role
def role_required(name: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_claims()
            if name not in claims['roles']:
                return jsonify(message="Unauthorized Access."), 403
            result = fn(*args, **kwargs)
            return result

        return wrapper

    return decorator
