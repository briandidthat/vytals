from datetime import datetime, date

from werkzeug.security import generate_password_hash

from vytals import db


class User(db.Model):
    """
    User model class to provide database mapping for user.
    - serialize: returns a dictionary representation of class attributes for easy JSONification.
    - age: (property) will return a formatted calculation of age based on birthdate
    """
    __tablename__ = 'user'
    id: int = db.Column(db.Integer, primary_key=True)
    first_name: str = db.Column(db.String(50), nullable=False)
    last_name: str = db.Column(db.String(100), nullable=False)
    username: str = db.Column(db.String(50), nullable=False, unique=True)
    password: str = db.Column(db.String(100), nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    birthdate: date = db.Column(db.Date, nullable=False)
    roles: list = db.relationship('Role', secondary='user_role', lazy='select', backref=db.backref('user', lazy=True))
    readings: list = db.relationship('Reading', backref='user', lazy=True)
    activities: list = db.relationship('Activity', backref='user', lazy=True)

    def __init__(self, first_name: str, last_name: str, username: str, password: str, email: str, birthdate: str):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.birthdate = date.fromisoformat(birthdate)

    def serialize(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "username": self.username,
            "email": self.email,
            "birthdate": str(self.birthdate)
        }


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

    def __init__(self, weight: float, blood_pressure: int, temperature: float, oxygen_level: int, pulse: int,
                 timestamp: str, user_id: int):
        self.weight = weight
        self.blood_pressure = blood_pressure
        self.temperature = temperature
        self.oxygen_level = oxygen_level
        self.pulse = pulse
        self.timestamp = datetime.fromisoformat(timestamp)
        self.user_id = user_id

    def serialize(self):
        return {
            "weight": self.weight,
            "bloodPressure": self.blood_pressure,
            "temperature": self.temperature,
            "oxygenLevel": self.oxygen_level,
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

    def __init__(self, type: str, description: str, start_time: str, end_time: str, user_id: int):
        self.type = type
        self.description = description
        self.start_time = datetime.fromisoformat(start_time)
        self.end_time = datetime.fromisoformat(end_time)
        self.user_id = user_id

    def serialize(self):
        return {
            "type": self.type,
            "description": self.description,
            "startTime": str(self.start_time),
            "endTime": str(self.end_time)
        }


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name: str):
        self.name = name


user_role = db.Table('user_role',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True))
