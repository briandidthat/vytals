from datetime import date


def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    return age


def parse_user(JSON):
    first_name = JSON.get('first_name', None)
    last_name = JSON.get('last_name', None)
    birthdate = JSON.get('birthdate', None)
    email = JSON.get('email', None)

    from models import User
    return User(first_name, last_name, date.fromisoformat(birthdate), email)


def parse_reading(JSON):
    weight = JSON.get('weight', None)
    blood_pressure = JSON.get('blood_pressure', None)
    temperature = JSON.get('temperature', None)
    pulse = JSON.get('pulse', None)
    user_id = JSON.get('user_id', None)

    from models import Reading
    return Reading(weight, blood_pressure, temperature, pulse, user_id)
