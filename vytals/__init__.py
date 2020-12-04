from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .exceptions import InvalidUsage

# instantiate db object
db = SQLAlchemy()


def init_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    with app.app_context():
        # initialize application db
        db.init_app(app)

        jwt = JWTManager(app=app)

        @app.errorhandler(InvalidUsage)
        def invalid_usage(error):
            response = jsonify(error.to_dict())
            response.status_code = error.status_code
            return response

        # will allow us to pass userId and roles via the token
        @jwt.user_claims_loader
        def add_claims_to_access_token(user):
            return {
                'id': user.id,
                "username": user.username,
                "roles": [role.name for role in user.roles]
            }

        @jwt.user_identity_loader
        def user_identity_lookup(user):
            return user.username

        # import and register blueprints
        from vytals.views import main, reading, activity
        app.register_blueprint(main)
        app.register_blueprint(reading)
        app.register_blueprint(activity)

    return app
