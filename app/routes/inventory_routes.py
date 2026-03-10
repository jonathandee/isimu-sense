from flask import render_template, request, redirect, url_for
from . import main
from .. import db
from ..models import InventoryCategory, InventoryItem


################################################
# INVENTORY DASHBOARD
################################################

@main.route("/inventory")
def inventory():
    return render_template("inventory.html")


################################################
# INVENTORY CATEGORIES (CONFIGURATION)
################################################

@main.route("/inventory/categories", methods=["GET", "POST"])
def inventory_categories():

    if request.method == "POST":

        name = request.form.get("name")

        category = InventoryCategory(name=name)

        db.session.add(category)
        db.session.commit()

        return redirect(url_for("main.inventory_categories"))

    categories = InventoryCategory.query.all()

    return render_template(
        "inventory_categories.html",
        categories=categories
    )


# EDIT INVENTORY CATEGORY
@main.route("/inventory/categories/edit/<int:id>", methods=["POST"])
def edit_inventory_category(id):

    category = InventoryCategory.query.get_or_404(id)

    category.name = request.form.get("name")

    db.session.commit()

    return redirect(url_for("main.inventory_categories"))


# DELETE INVENTORY CATEGORY (Allowed: configuration entity)
@main.route("/inventory/categories/delete/<int:id>")
def delete_inventory_category(id):

    category = InventoryCategory.query.get_or_404(id)

    db.session.delete(category)
    db.session.commit()

    return redirect(url_for("main.inventory_categories"))


################################################
# INVENTORY ITEMS (STOCK MANAGEMENT)
################################################

@main.route("/inventory/items", methods=["GET", "POST"])
def inventory_items():

    categories = InventoryCategory.query.all()

    if request.method == "POST":

        name = request.form.get("name")
        category_id = request.form.get("category")
        quantity = request.form.get("quantity")
        unit = request.form.get("unit")

        item = InventoryItem(
            name=name,
            category_id=category_id,
            quantity=quantity,
            unit=unit
        )

        db.session.add(item)
        db.session.commit()

        return redirect(url_for("main.inventory_items"))

    items = InventoryItem.query.all()

    return render_template(
        "inventory_items.html",
        items=items,
        categories=categories
    )


# EDIT INVENTORY ITEM
@main.route("/inventory/items/edit/<int:id>", methods=["POST"])
def edit_inventory_item(id):

    item = InventoryItem.query.get_or_404(id)

    item.name = request.form.get("name")
    item.category_id = request.form.get("category")
    item.quantity = request.form.get("quantity")
    item.unit = request.form.get("unit")

    db.session.commit()

    return redirect(url_for("main.inventory_items"))


# DELETE INVENTORY ITEM
@main.route("/inventory/items/delete/<int:id>")
def delete_inventory_item(id):

    item = InventoryItem.query.get_or_404(id)

    db.session.delete(item)
    db.session.commit()

    return redirect(url_for("main.inventory_items"))