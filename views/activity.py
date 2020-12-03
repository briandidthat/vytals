from flask import Blueprint, request, jsonify, render_template, redirect, url_for

from app import db
from exceptions import InvalidUsage
from models import Activity, User
from utils import parse_activity
from forms import ActivityForm

activity = Blueprint('activity', __name__)


@activity.route('/activities/user/new', methods=['GET', 'POST'])
def create_activity():
    form = ActivityForm()
    if form.validate_on_submit():
        activity = parse_activity(request.json)
        user = User.query.filter_by(user_id=id).first()

        if user is None:
            raise InvalidUsage("Sorry, that user does not exist.", status_code=404)

        activity.user_id = user.id
        db.session.add(activity)
        db.session.commit()
        return redirect(url_for('get_activities'))
    return render_template('add-activity.html', form=form)


@activity.route('/activities/user/<int:id>/all', methods=['GET'])
def get_activities(id):
    activities = Activity.query.filter_by(user_id=id).all()

    if len(activities) == 0:
        raise InvalidUsage(f"There are no readings associated with the id {id}.", status_code=404)

    return render_template('activities.html', activities=activities)
