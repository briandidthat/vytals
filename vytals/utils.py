from datetime import datetime
from functools import wraps

from cerberus import Validator
from email_validator import validate_email, EmailNotValidError
from flask import jsonify
from flask_jwt_extended import get_jwt_claims, verify_jwt_in_request

from vytals.exceptions import InvalidUsage

to_date = lambda s: datetime.strptime(s, '%Y-%m-%d')
to_date_time = lambda s: datetime.fromisoformat(s)
sort_by_date = lambda x: datetime.strptime(x['timestamp'], '%Y/%m/%d %H:%M:%S')


def test_email_address(email: str):
    try:
        valid = validate_email(email)
        return str(valid.email)
    except EmailNotValidError as e:
        raise InvalidUsage(message=str(e), status_code=422)


# will parse user data from json and return User instance
def parse_user(JSON: dict):
    first_name = JSON.get('firstName', None)
    last_name = JSON.get('lastName', None)
    username = JSON.get('username', None)
    password = JSON.get('password', None)
    email = JSON.get('email', None)
    birthdate = JSON.get('birthdate', None)

    from vytals.models import User
    return User(first_name, last_name, username, password, email, birthdate)


# will parse reading data from json and return Reading instance
def parse_reading(JSON: dict, user_id: int):
    weight = JSON.get('weight', None)
    blood_pressure = JSON.get('bloodPressure', None)
    temperature = JSON.get('temperature', None)
    oxygen_level = JSON.get('oxygenLevel', None)
    pulse = JSON.get('pulse', None)
    timestamp = JSON.get('timestamp', None)

    from vytals.models import Reading
    return Reading(weight, blood_pressure, temperature, oxygen_level, pulse, timestamp, user_id)


# will parse activity data from json and return Activity instance
def parse_activity(JSON: dict, user_id: int):
    type = JSON.get('type', None)
    description = JSON.get('description', None)
    start_time = JSON.get('startTime', None)
    end_time = JSON.get('endTime', None)

    from vytals.models import Activity
    return Activity(type, description, start_time, end_time, user_id)


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
    'firstName': {
        'type': 'string'
    },
    'lastName': {
        'type': 'string'
    },
    'username': {
        'type': 'string'
    },
    'password': {
        'type': 'string'
    },
    'email': {
        'type': 'string',
        'coerce': test_email_address,
    },
    'birthdate': {
        'type': 'date',
        'coerce': to_date
    }
}

user_validator = Validator(user_schema)

reading_schema = {
    'weight': {
        'type': 'number'
    },
    'bloodPressure': {
        'type': 'number'
    },
    'temperature': {
        'type': 'number'
    },
    'oxygenLevel': {
        'type': 'number'
    },
    'pulse': {
        'type': 'number'
    },
    'timestamp': {
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

