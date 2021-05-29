from datetime import datetime

from flask import Flask, session


def create_app():
    app = Flask(__name__)
    load_configuration(app)
    app.secret_key = bytes.fromhex(app.config['FLASK_SECRET'])
    register_extensions(app)
    register_blueprints(app)
    return app


def load_configuration(app):
    app.config.from_object('config')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{app.config.get('DB_USER')}:{app.config.get('DB_PASSWORD')}@{app.config.get('DB_HOST')}/{app.config.get('DB_NAME')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def register_extensions(app):

    from extensions.db import db
    from extensions.limiter import limiter
    from extensions.migrate import migrate

    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)



def register_blueprints(app):
    from routes.web import web_bp
    app.register_blueprint(web_bp)
    pass



app = create_app()


@app.before_request
def make_session_permanent():
    if session.get('cookies_accepted'):
        session.permanent = True


if __name__ == "__main__":
    app.run(host='0.0.0.0')
