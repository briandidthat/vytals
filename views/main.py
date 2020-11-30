from flask import Blueprint, request, jsonify

from app import db
from exceptions import InvalidUsage
from models import Activity, User, Reading
from utils import (parse_user, parse_reading, parse_activity, activity_validator, reading_validator, user_validator)

main = Blueprint('main', __name__)


@main.route('/users/new', methods=['POST'])
def create_user():
    if not user_validator.validate(request.json):
        raise InvalidUsage(user_validator.errors, status_code=422)

    data = parse_user(request.json)
    user = User.query.filter_by(email=data.email).first()

    if user:
        raise InvalidUsage("That user already exists in the system.", status_code=409)

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
        raise InvalidUsage(reading_validator.errors, status_code=422)

    reading = parse_reading(request.json)
    user = User.query.filter_by(id=reading.user_id).first()

    if user is None:
        raise InvalidUsage("Sorry, that user does not exist.", status_code=404)

    db.session.add(reading)
    db.session.commit()

    return jsonify(reading=reading.serialize()), 201


@main.route('/readings/user/all/<int:id>', methods=['GET'])
def get_readings(id):
    readings = Reading.query.filter_by(user_id=id).all()

    if len(readings) == 0:
        raise InvalidUsage(f"There are no activities associated with id {id}.", status_code=404)

    return jsonify(readings=[r.serialize() for r in readings]), 200


@main.route('/activities/user/new', methods=['POST'])
def create_activity(id):
    if not activity_validator.validate(request.json):
        raise InvalidUsage(activity_validator.errors, status_code=422)

    activity = parse_activity(request.json)
    user = User.query.filter_by(user_id=id).first()

    if user is None:
        raise InvalidUsage("Sorry, that user does not exist.", status_code=404)

    activity.user_id = id
    db.session.add(activity)
    db.session.commit()

    return jsonify(activity=activity.serialize()), 201


@main.route('/activities/user/all/<int:id>', methods=['GET'])
def get_activities(id):
    activities = Activity.query.filter_by(user_id=id).all()

    if len(activities) == 0:
        raise InvalidUsage(f"There are no readings associated with the id {id}.", status_code=404)

    return jsonify(activities=[a.serialize() for a in activities]), 200


@main.errorhandler(InvalidUsage)
def invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
