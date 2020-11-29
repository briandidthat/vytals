from datetime import date, datetime

from cerberus import Validator


# will calculate age based on current date - birthdate
def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    return age


# will parse user data from json and return User instance
def parse_user(JSON):
    first_name = JSON.get('first_name', None)
    last_name = JSON.get('last_name', None)
    birthdate = JSON.get('birthdate', None)
    email = JSON.get('email', None)

    from models import User
    return User(first_name, last_name, date.fromisoformat(birthdate), email)


# will parse reading data from json and return Reading instance
def parse_reading(JSON):
    weight = JSON.get('weight', None)
    blood_pressure = JSON.get('blood_pressure', None)
    temperature = JSON.get('temperature', None)
    oxygen_level = JSON.get('oxygen_level', None)
    pulse = JSON.get('pulse', None)
    datetime = JSON.get('date_time', None)
    user_id = JSON.get('user_id', None)

    from models import Reading
    return Reading(weight, blood_pressure, temperature, oxygen_level, pulse, datetime, user_id)


# will parse activity data from json and return Activity instance
def parse_activity(JSON):
    type = JSON.get('type', None)
    duration = JSON.get('duration', None)
    description = JSON.get('description', None)
    date_time = JSON.get('datetime', None)
    user_id = JSON.get('user_id', None)

    from models import Activity
    return Activity(type, duration, description, date_time, user_id)


user_schema = {
    'first_name': {
        'type': 'string'
    },
    'last_name': {
        'type': 'string'
    },
    'birthdate': {
        'type': 'string'
    },
    'email': {
        'type': 'string'
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
    'datetime': {
        'type': 'datetime'
    },
    'user_id': {
        'type': 'number'
    }
}

reading_validator = Validator(reading_schema)

activity_schema = {
    'type': {
        'type': 'string'
    },
    'duration': {
        'type': 'string'
    },
    'description': {
        'type': 'string'
    },
    'datetime': {
        'type': 'datetime'
    },
    'user_id': {
        'type': 'number'
    }
}

activity_validator = Validator(activity_schema)
