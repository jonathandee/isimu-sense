from flask import Blueprint

# Main blueprint for the application
main = Blueprint("main", __name__)

# Import route modules (registers routes with blueprint)
from .dashboard_routes import *
from .crop_routes import *
from .inventory_routes import *
from .livestock_routes import *
from .finance_routes import *
from .reports_routes import *