from flask import Blueprint
from .models import InventoryCategory
from . import db

main = Blueprint("main", __name__)

@main.route("/")
def home():
    categories = InventoryCategory.query.all()

    output = "<h1>Inventory Categories</h1><ul>"
    for category in categories:
        output += f"<li>{category.name} - {category.description}</li>"
    output += "</ul>"

    return output