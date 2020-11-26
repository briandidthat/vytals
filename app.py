from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# instantiate db object
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    # initialize application db
    db.init_app(app)

    # import and register blueprints
    from views import main
    app.register_blueprint(main)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
