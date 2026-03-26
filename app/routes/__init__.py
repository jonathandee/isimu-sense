from flask import Blueprint, redirect, url_for, request
from flask_login import current_user

main = Blueprint("main", __name__)

@main.before_request
def require_login():

    # ✅ Skip static files
    if request.endpoint == "static":
        return

    # ✅ Skip if endpoint is missing (prevents crash/loop)
    if request.endpoint is None:
        return

    # ✅ Allow login route
    if request.endpoint == "main.login":
        return

    # ✅ Allow logout
    if request.endpoint == "main.logout":
        return

    # ✅ If not logged in → redirect
    if not current_user.is_authenticated:
        return redirect(url_for("main.login"))


from .auth_routes import *
from .crop_routes import *
from .inventory_routes import *
from .livestock_routes import *
from .finance_routes import *
from .reports_routes import *
from .weather_routes import *