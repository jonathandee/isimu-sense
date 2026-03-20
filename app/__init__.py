from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app():

    app = Flask(__name__)

    # ✅ Load config FIRST
    env = os.getenv("FLASK_ENV", "development")

    if env == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    # ✅ THEN initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "main.login"

    # ✅ Register blueprint
    from .routes import main
    app.register_blueprint(main)

    return app


# ✅ Import AFTER db is defined
from .models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))