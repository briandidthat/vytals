from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from vytals import db
from vytals.exceptions import InvalidUsage
from vytals.models import Activity, User
from vytals.utils import parse_activity, activity_validator, role_required

activity = Blueprint('activity', __name__)


# @role_required('USER')
@activity.route('/activities/user/<int:id>/new', methods=['GET', 'POST'])
def create_activity(id: int):
    if not activity_validator.validate(request.json):
        raise InvalidUsage(activity_validator.errors, status_code=422)

    user = User.query.filter_by(id=id).first()
    if user is None:
        raise InvalidUsage("There is no user associated with the id provided.", status_code=404)

    activity = parse_activity(request.json, user.id)
    db.session.add(activity)

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise InvalidUsage("Internal server error.", status_code=500)

    return jsonify(activity=activity.serialize()), 201


@activity.route('/activities/user/<int:id>/all', methods=['GET'])
def get_activities(id: int):
    activities = Activity.query.filter_by(user_id=id).all()

    if len(activities) == 0:
        raise InvalidUsage("There are no readings associated with the id provided.", status_code=404)

    return jsonify(activities=[a.serialize() for a in activities])
