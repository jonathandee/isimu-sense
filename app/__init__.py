from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Extensions
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

    # ✅ Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "main.login"

    # ✅ Register blueprint
    from .routes import main
    app.register_blueprint(main)

    # ✅ Import models AFTER db init
    from .models import Planting, Harvest, InventoryItem, Field

    # ✅ CONTEXT PROCESSOR (THIS IS THE FIX)
    @app.context_processor
    def inject_stats():
        return {
            "active_plantings": Planting.query.filter_by(status="active").count(),
            "total_harvest": db.session.query(db.func.sum(Harvest.quantity)).scalar() or 0,
            "inventory_count": InventoryItem.query.count(),
            "field_count": Field.query.count()
        }

    return app


# ✅ Import User AFTER db is defined
from .models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))