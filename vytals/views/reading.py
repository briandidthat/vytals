from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from vytals import db
from vytals.exceptions import InvalidUsage
from vytals.models import Reading, User
from vytals.utils import parse_reading, reading_validator, role_required

reading = Blueprint('reading', __name__)


@reading.route('/readings/user/<int:id>/new', methods=['POST'])
@role_required("USER")
def create_reading(id: int):
    if not reading_validator.validate(request.json):
        raise InvalidUsage(reading_validator.errors, status_code=404)

    user = User.query.filter_by(id=id).first()

    if user is None:
        raise InvalidUsage("There is no user associated with the id provided.", status_code=404)

    reading = parse_reading(request.json, user.id)
    db.session.add(reading)
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise InvalidUsage("Internal server error. Try again", 500)
    return jsonify(reading=reading.serialize()), 201


@reading.route('/readings/user/<int:id>/all', methods=['GET'])
@role_required("USER")
def get_readings(id: int):
    readings = Reading.query.filter_by(user_id=id).all()

    if len(readings) == 0:
        raise InvalidUsage("There are no readings associated with the id provided.", status_code=404)

    # will return readings in ascending order by date
    sorted_readings = sorted(readings, key=lambda x: x.timestamp)

    return jsonify(readings=[r.serialize() for r in sorted_readings]), 200
