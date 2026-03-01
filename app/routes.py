from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/")
def landing():
    return render_template("index.html")

@main.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@main.route("/inventory")
def inventory():
    from .models import InventoryCategory
    categories = InventoryCategory.query.all()
    return render_template("inventory.html", categories=categories)

@main.route("/crops")
def crops():
    return render_template("crops.html")

@main.route("/livestock")
def livestock():
    return render_template("livestock.html")

@main.route("/finance")
def finance():
    return render_template("finance.html")

@main.route("/reports")
def reports():
    return render_template("reports.html")
