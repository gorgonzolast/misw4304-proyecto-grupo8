import os
from dotenv import load_dotenv
from flask import Flask
from .routes.blacklist_bp import blacklist_bp
from .config.config import Config, TestingConfig
from .models.models import db


def create_app():
    load_dotenv()

    app = Flask(__name__)

    if os.getenv("FLASK_ENV") == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)

    app.register_blueprint(blacklist_bp)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
