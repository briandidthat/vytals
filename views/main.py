from flask import Blueprint, request, jsonify

from app import db
from models import User
from utils import (parse_user, parse_reading, parse_activity, activity_validator, reading_validator, user_validator)

main = Blueprint('main', __name__)


@main.route('/users/new', methods=['POST'])
def create_user():
    if not user_validator.validate(request.json):
        print(type(request.json['birthdate']))
        raise ValueError(user_validator.errors)

    data = parse_user(request.json)
    user = User.query.filter_by(email=data.email).first()

    if user:
        raise ValueError("That user already exists in the system.")

    db.session.add(data)
    db.session.commit()
    return jsonify(user=data.serialize()), 201


@main.route('/users/all', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify(users=[u.serialize() for u in users]), 200


@main.route('/readings/user/new', methods=['POST'])
def create_reading():
    if not reading_validator.validate(request.json):
        raise ValueError(reading_validator.errors)

    reading = parse_reading(request.json)
    user = User.query.filter_by(id=reading.user_id).first()

    if user is None:
        raise LookupError("Sorry, that user does not exist.")

    reading.user_id = user.id
    db.session.add(reading)
    db.session.commit()

    return jsonify(reading=reading.serialize()), 201


@main.route('/activities/user/new', methods=['POST'])
def create_activity(id):
    if not activity_validator.validate(request.json):
        raise ValueError(activity_validator.errors)

    activity = parse_activity(request.json)
    user = User.query.filter_by(user_id=id).first()

    if user is None:
        raise LookupError("Sorry, that user does not exist.")

    activity.user_id = id
    db.session.add(activity)
    db.session.commit()

    return jsonify(activity=activity.serialize()), 201
