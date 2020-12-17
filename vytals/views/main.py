from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash

from vytals import db
from vytals.exceptions import InvalidUsage
from vytals.models import User, Role
from vytals.utils import parse_user, user_validator, login_validator

main = Blueprint('main', __name__)


@main.route('/users/login', methods=['POST'])
def login():
    if not login_validator(request.json):
        raise InvalidUsage(user_validator.errors, status_code=422)

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        raise InvalidUsage("Invalid login credentials.", 401)

    access_token = create_access_token(user)
    return jsonify(access_token=access_token), 200


@main.route('/users/new', methods=['POST'])
def register():
    if not user_validator.validate(request.json):
        raise InvalidUsage(user_validator.errors, status_code=422)

    user_exists = User.query.filter_by(username=request.json.get('username')).first()

    if user_exists:
        raise InvalidUsage("That user already exists in the system.", status_code=409)

    user = parse_user(request.json)
    role = Role.query.filter_by(name='USER').first()
    user.roles.append(role)
    db.session.add(user)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        if "UNIQUE constraint failed: user.email" in str(e):
            raise InvalidUsage("Error. That email address already exists.", status_code=409)

    access_token = create_access_token(user)
    return jsonify(access_token=access_token), 201


@main.route('/users/all', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify(users=[u.serialize() for u in users]), 200
