from flask import Flask, session

import os


def create_app():
    app = Flask(__name__)
    load_configuration(app)
    app.secret_key = bytes.fromhex(app.config['FLASK_SECRET'])
    register_extensions(app)
    register_blueprints(app)
    return app


def load_configuration(app):
    if os.environ.get("APPLICATION_MODE") == "DEV":
        app.config.from_object('config.DevelopmentConfig')
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{app.config.get('DB_USER')}:{app.config.get('DB_PASSWORD')}@{app.config.get('DB_HOST')}/{app.config.get('DB_NAME')}"
    elif os.environ.get("APPLICATION_MODE") == "PROD":
        app.config.from_object('config.ProductionConfig')
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 10

def register_extensions(app):

    from extensions.db import db
    from extensions.limiter import limiter
    from extensions.migrate import migrate
    from extensions.login import login_manager
    from extensions.jinja_functions import jinja_functions
    from extensions.image_service import image_service

    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    login_manager.init_app(app)
    jinja_functions.init_app(app)
    image_service.init_app(app)


def register_blueprints(app):
    from routes.login import login_bp
    from routes.room import room_bp
    from routes.profile import profile_bp
    from routes.feedback import feedback_bp

    app.register_blueprint(login_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(feedback_bp)


app = create_app()


@app.before_request
def make_session_permanent():
    if session.get('cookies_accepted'):
        session.permanent = True


if __name__ == "__main__":
    app.run(host='0.0.0.0')
