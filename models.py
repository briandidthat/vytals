from app import db
from utils import calculate_age


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
    birthday = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    readings = db.relationship('Reading', backref='user', lazy=True)
    activities = db.relationship('Excercise', backref='user', lazy=True)

    def __init__(self, first_name, last_name, birthdate, email):
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.email = email

    def serialize(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email
        }

    @property
    def age(self):
        return calculate_age(self.birthdate)


class Reading(db.Model):
    """
    Reading model class to provide database mapping to vital readings.
    - serialize: returns a dictionary representation of class attributes for easy JSONification.
    """
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    blood_pressure = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    pulse = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, weight, blood_pressure, temperature, user_id):
        self.weight = weight
        self.blood_pressure = blood_pressure
        self.temperature = temperature
        self.user_id = user_id

    def serialize(self):
        return {
            "weight": self.weight,
            "blood_pressure": self.blood_pressure,
            "temperature": self.temperature,
            "pulse": self.pulse
        }


class Activity(db.Model):
    """
    Activity model class to provide database mapping to activities.
    - serialize: returns a dictionary representation of class attributes for easy JSONificiation
    """
    id = db.Column(db.Integer, primary_key=True)
    type = db.String(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    description = db.String(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, date, time, type, description, user_id):
        self.date = date
        self.time = time
        self.type = type
        self.description = description
        self.user_id = user_id

    def serialize(self):
        return {
            "type": self.type,
            "date": str(self.date),
            "time": str(self.time),
            "description": self.description
        }
