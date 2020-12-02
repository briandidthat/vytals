from flask import Flask, jsonify
from exceptions import InvalidUsage
from flask_sqlalchemy import SQLAlchemy

# instantiate db object
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    # initialize application db
    db.init_app(app)

    @app.errorhandler(InvalidUsage)
    def invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    # import and register blueprints
    from views import main, reading, activity
    app.register_blueprint(main)
    app.register_blueprint(reading)
    app.register_blueprint(activity)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
