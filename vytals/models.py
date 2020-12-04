from werkzeug.security import generate_password_hash

from vytals import db
from .utils import calculate_age, calculate_duration


class User(db.Model):
    """
    User model class to provide database mapping for user.
    - serialize: returns a dictionary representation of class attributes for easy JSONification.
    - age: (property) will return a formatted calculation of age based on birthdate
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    roles = db.relationship('Role', secondary='user_role', lazy='select', backref=db.backref('user', lazy=True))
    readings = db.relationship('Reading', backref='user', lazy=True)
    activities = db.relationship('Activity', backref='user', lazy=True)

    def __init__(self, first_name, last_name, username, password, email, birthdate):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.birthdate = birthdate

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "age": self.age
        }

    @property
    def age(self):
        return calculate_age(self.birthdate)


class Reading(db.Model):
    """
    Reading model class to provide database mapping to vital readings.
    - serialize: returns a dictionary representation of class attributes for easy JSONification.
    """
    __tablename_ = 'reading'
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    blood_pressure = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    oxygen_level = db.Column(db.Float, nullable=False)
    pulse = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, weight, blood_pressure, temperature, oxygen_level, pulse, timestamp, user_id):
        self.weight = weight
        self.blood_pressure = blood_pressure
        self.temperature = temperature
        self.oxygen_level = oxygen_level
        self.pulse = pulse
        self.timestamp = timestamp
        self.user_id = user_id

    def serialize(self):
        return {
            "weight": self.weight,
            "blood_pressure": self.blood_pressure,
            "temperature": self.temperature,
            "oxygen_level": self.oxygen_level,
            "pulse": self.pulse,
            "timestamp": str(self.timestamp)
        }


class Activity(db.Model):
    """
    Activity model class to provide database mapping to activities.
    - serialize: returns a dictionary representation of class attributes for easy JSONificiation.
    - duration (property): returns duration in [minutes: seconds] format.
    """
    __tablename__ = 'activity'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, type, description, start_time, end_time, user_id):
        self.type = type
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.user_id = user_id

    def serialize(self):
        return {
            "type": self.type,
            "description": self.description,
            "start_time": str(self.start_time),
            "end_time": str(self.end_time),
            "duration": self.duration
        }

    @property
    def duration(self):
        minutes, seconds = calculate_duration(self.start_time, self.end_time)

        return f"{minutes} minutes:{seconds} seconds"


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        self.name = name


user_role = db.Table('user_role',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True))
