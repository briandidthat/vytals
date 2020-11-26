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
