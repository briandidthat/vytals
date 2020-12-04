from flask import Blueprint, request, jsonify

from vytals import db
from vytals.exceptions import InvalidUsage
from vytals.models import User, Role
from vytals.utils import parse_user, user_validator, role_required

main = Blueprint('main', __name__)


@main.route('/users/new', methods=['POST'])
def create_user():
    if not user_validator.validate(request.json):
        raise InvalidUsage(user_validator.errors, status_code=422)

    data = parse_user(request.json)

    user = User.query.filter_by(username=data.username).first()
    role = Role.query.get(1)  # 1 will always represent the USER role

    if user:
        raise InvalidUsage("That user already exists in the system.", status_code=409)

    data.roles.append(role)
    db.session.add(data)
    db.session.commit()
    return jsonify(user=data.serialize()), 201


@main.route('/users/all', methods=['GET'])
@role_required("ADMIN")
def get_all_users():
    users = User.query.all()
    return jsonify(users=[u.serialize() for u in users]), 200
