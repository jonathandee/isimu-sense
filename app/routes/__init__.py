from flask import Blueprint, redirect, url_for, request
from flask_login import current_user

main = Blueprint("main", __name__)

@main.before_request
def require_login():

    # Allow login, logout and static files
    if request.endpoint in ["main.login", "main.logout", "static"]:
        return

    # If user not authenticated redirect to login
    if not current_user.is_authenticated:
        return redirect(url_for("main.login"))


from .auth_routes import *
from .dashboard_routes import *
from .crop_routes import *
from .inventory_routes import *
from .livestock_routes import *
from .finance_routes import *
from .reports_routes import *