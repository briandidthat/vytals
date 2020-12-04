from flask import Blueprint, request, jsonify

from vytals import db
from vytals.exceptions import InvalidUsage
from vytals.models import Activity, User
from vytals.utils import parse_activity, activity_validator

activity = Blueprint('activity', __name__)


@activity.route('/activities/user/<int:id>/new', methods=['GET', 'POST'])
def create_activity(id: int):
    if not activity_validator.validate(request.json):
        raise InvalidUsage(activity_validator.errors, status_code=422)
    activity = parse_activity(request.json)
    user = User.query.filter_by(user_id=id).first()

    if user is None:
        raise InvalidUsage("There is no user associated with the id provided.", status_code=404)

    activity.user_id = user.id
    db.session.add(activity)
    db.session.commit()
    return jsonify(activity=activity.serialize()), 201


@activity.route('/activities/user/<int:id>/all', methods=['GET'])
def get_activities(id: int):
    activities = Activity.query.filter_by(user_id=id).all()

    if len(activities) == 0:
        raise InvalidUsage("There are no readings associated with the id provided.", status_code=404)

    return jsonify(activities=[a.serialize() for a in activities])
