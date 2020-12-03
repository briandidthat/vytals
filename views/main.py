from flask import Blueprint, request, jsonify

from app import db
from exceptions import InvalidUsage
from models import User
from utils import parse_user

main = Blueprint('main', __name__)


@main.route('/users/new', methods=['POST'])
def create_user():
    # if not user_validator.validate(request.json):
    #     raise InvalidUsage(user_validator.errors, status_code=422)

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
