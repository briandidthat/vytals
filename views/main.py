from flask import Blueprint, request, jsonify
from app import db
from models import User
from utils import parse_user

main = Blueprint('main', __name__)


@main.route('/users', methods=['POST'])
def create_user():
    data = parse_user(request.json)

    user = User.query.filter_by(email=data.email).first()

    if user:
        raise ValueError("That user already exists in the system.")

    db.session.add(data)
    db.session.commit()

    return jsonify(user=data.serialize()), 201
