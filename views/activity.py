from flask import Blueprint, request, jsonify, render_template

from app import db
from exceptions import InvalidUsage
from models import Activity, User
from utils import parse_activity, activity_validator

activity = Blueprint('activity', __name__)


@activity.route('/activities/user/<int:id>/new', methods=['POST'])
def create_activity(id: int):
    if not activity_validator.validate(request.json):
        raise InvalidUsage(activity_validator.errors, status_code=422)

    activity = parse_activity(request.json)
    user = User.query.filter_by(user_id=id).first()

    if user is None:
        raise InvalidUsage("Sorry, that user does not exist.", status_code=404)

    activity.user_id = user.id
    db.session.add(activity)
    db.session.commit()

    return jsonify(activity=activity.serialize()), 201


@activity.route('/activities/user/<int:id>/all', methods=['GET'])
def get_activities(id):
    activities = Activity.query.filter_by(user_id=id).all()

    if len(activities) == 0:
        raise InvalidUsage(f"There are no readings associated with the id {id}.", status_code=404)

    return render_template('activities.html', activities=activities)
