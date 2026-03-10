from flask import render_template
from .. import db
from ..models import Planting, Harvest, InventoryItem, Field
from . import main


##################################
# LANDING PAGE
##################################

@main.route("/")
def landing():
    return render_template("index.html")


##################################
# DASHBOARD
##################################

@main.route("/dashboard")
def dashboard():

    active_plantings = Planting.query.filter_by(status="active").count()

    total_harvest = db.session.query(
        db.func.sum(Harvest.quantity)
    ).scalar() or 0

    inventory_count = InventoryItem.query.count()

    field_count = Field.query.count()

    return render_template(
        "dashboard.html",
        active_plantings=active_plantings,
        total_harvest=total_harvest,
        inventory_count=inventory_count,
        field_count=field_count
    )