from datetime import date, datetime

from cerberus import Validator


def calculate_duration(start_time: datetime, end_time: datetime):
    if not all(isinstance(i, datetime) for i in [start_time, end_time]):
        raise ValueError("Invalid type.")

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
    birthdate_string = JSON.get('birthdate', None)
    birthdate = date.fromisoformat(birthdate_string)
    email = JSON.get('email', None)

    from models import User
    return User(first_name, last_name, birthdate, email)


# will parse reading data from json and return Reading instance
def parse_reading(JSON: dict):
    weight = JSON.get('weight', None)
    blood_pressure = JSON.get('blood_pressure', None)
    temperature = JSON.get('temperature', None)
    oxygen_level = JSON.get('oxygen_level', None)
    pulse = JSON.get('pulse', None)
    date_time = JSON.get('date_time', None)
    timestamp = datetime.fromisoformat(date_time)  # convert string to datetime object

    from models import Reading
    return Reading(weight, blood_pressure, temperature, oxygen_level, pulse, timestamp, None)


# will parse activity data from json and return Activity instance
def parse_activity(JSON: dict):
    type = JSON.get('type', None)
    description = JSON.get('description', None)
    start_time = JSON.get('start_time', None)
    end_time = JSON.get('end_time', None)
    start_datetime = datetime.fromisoformat(start_time)  # convert string to datetime object
    end_datetime = datetime.fromisoformat(end_time)   # convert string to datetime object

    from models import Activity
    return Activity(type, description, start_datetime, end_datetime,  None)


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
    'date_time': {
        'type': 'string'
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
        'type': 'string'
    },
    'end_time': {
        'type': 'string'
    }
}

activity_validator = Validator(activity_schema)
