from flask import Blueprint, render_template
from flask import request, redirect, url_for
from datetime import datetime
from .models import CropType
from .models import Field
from .models import Planting
from datetime import datetime
from .models import InventoryCategory
from .models import InventoryItem
from .models import Application
from flask import flash  
from .models import Harvest
from . import db

main = Blueprint("main", __name__)

@main.route("/")
def landing():
    return render_template("index.html")

@main.route("/dashboard")
def dashboard():

    active_plantings = Planting.query.filter_by(status="active").count()

    total_harvest = db.session.query(db.func.sum(Harvest.quantity)).scalar() or 0

    inventory_count = InventoryItem.query.count()

    field_count = Field.query.count()

    return render_template(
        "dashboard.html",
        active_plantings=active_plantings,
        total_harvest=total_harvest,
        inventory_count=inventory_count,
        field_count=field_count
    )

##################################
        # INVENTORY #
##################################

@main.route("/inventory")
def inventory():
    return render_template("inventory.html")

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

@main.route("/inventory/categories/edit/<int:id>", methods=["POST"])
def edit_inventory_category(id):

    category = InventoryCategory.query.get_or_404(id)

    category.name = request.form.get("name")

    db.session.commit()

    return redirect(url_for("main.inventory_categories"))

@main.route("/inventory/categories/delete/<int:id>")
def delete_inventory_category(id):

    category = InventoryCategory.query.get_or_404(id)

    db.session.delete(category)
    db.session.commit()

    return redirect(url_for("main.inventory_categories"))

############ INVENTORY ITEMS ###########

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

@main.route("/inventory/items/edit/<int:id>", methods=["POST"])
def edit_inventory_item(id):

    item = InventoryItem.query.get_or_404(id)

    item.name = request.form.get("name")
    item.category_id = request.form.get("category")
    item.quantity = request.form.get("quantity")
    item.unit = request.form.get("unit")

    db.session.commit()

    return redirect(url_for("main.inventory_items"))

@main.route("/inventory/items/delete/<int:id>")
def delete_inventory_item(id):

    item = InventoryItem.query.get_or_404(id)

    db.session.delete(item)
    db.session.commit()

    return redirect(url_for("main.inventory_items"))


#############################################
                #CROPS MODULE#
#############################################

@main.route("/crops")
def crops():
    return render_template("crops.html")

@main.route("/crops/types", methods=["GET", "POST"])
def crop_types():
    if request.method == "POST":
        name = request.form.get("name")
        variety = request.form.get("variety")
        notes = request.form.get("notes")

        new_crop = CropType(
            name=name,
            variety=variety,
            notes=notes
        )

        db.session.add(new_crop)
        db.session.commit()

        return redirect(url_for("main.crop_types"))

    crops = CropType.query.all()
    return render_template("crop_types.html", crops=crops)

############ DELETE BUTTON ############

@main.route("/crops/types/delete/<int:id>")
def delete_crop_type(id):
    crop = CropType.query.get_or_404(id)

    db.session.delete(crop)
    db.session.commit()

    return redirect(url_for("main.crop_types"))

############ EDIT BUTTON ################

@main.route("/crops/types/edit/<int:id>", methods=["POST"])
def edit_crop_type(id):
    crop = CropType.query.get_or_404(id)

    crop.name = request.form.get("name")
    crop.variety = request.form.get("variety")
    crop.notes = request.form.get("notes")

    db.session.commit()

    return redirect(url_for("main.crop_types"))

#############################################
                #FIELDS MODULE#
#############################################

@main.route("/crops/fields", methods=["GET", "POST"])
def fields():

    if request.method == "POST":
        name = request.form.get("name")
        size = request.form.get("size")
        location = request.form.get("location")

        new_field = Field(
            name=name,
            size=size,
            location=location
        )

        db.session.add(new_field)
        db.session.commit()

        return redirect(url_for("main.fields"))

    fields = Field.query.all()

    return render_template("fields.html", fields=fields)

############ DELETE #############

@main.route("/crops/fields/delete/<int:id>")
def delete_field(id):

    field = Field.query.get_or_404(id)

    db.session.delete(field)
    db.session.commit()

    return redirect(url_for("main.fields"))

############ EDIT ############

@main.route("/crops/fields/edit/<int:id>", methods=["POST"])
def edit_field(id):

    field = Field.query.get_or_404(id)

    field.name = request.form.get("name")
    field.size = request.form.get("size")
    field.location = request.form.get("location")

    db.session.commit()

    return redirect(url_for("main.fields"))

####################################
            # PLANTINGS #
####################################

@main.route("/crops/plantings", methods=["GET", "POST"])
def plantings():

    crops = CropType.query.all()
    fields = Field.query.all()

    if request.method == "POST":

        crop_type_id = request.form.get("crop_type")
        field_id = request.form.get("field")

        planting_date = datetime.strptime(
            request.form.get("planting_date"),
            "%Y-%m-%d"
        )

        expected_harvest = datetime.strptime(
            request.form.get("expected_harvest"),
            "%Y-%m-%d"
        )

        # 🚫 Prevent planting on already planted field
        existing = Planting.query.filter_by(field_id=field_id, status="active").first()

        if existing:
            flash("This field already has an active planting.", "danger")
            return redirect(url_for("main.plantings"))

        new_planting = Planting(
            crop_type_id=crop_type_id,
            field_id=field_id,
            planting_date=planting_date,
            expected_harvest=expected_harvest
        )

        db.session.add(new_planting)
        db.session.commit()

        return redirect(url_for("main.plantings"))

    plantings = Planting.query.all()

    return render_template(
        "plantings.html",
        plantings=plantings,
        crops=crops,
        fields=fields
    )
    
############### STATUS ##############

@main.route("/crops/plantings/complete/<int:id>")
def complete_planting(id):

    planting = Planting.query.get_or_404(id)

    planting.status = "completed"

    db.session.commit()

    flash("Planting marked as completed.", "success")

    return redirect(url_for("main.plantings"))

##############################################
            ######APPLICATIONS########
##############################################

@main.route("/crops/applications", methods=["GET", "POST"])
def applications():

    plantings = Planting.query.all()
    inventory_items = InventoryItem.query.all()

    if request.method == "POST":

        planting_id = request.form.get("planting")
        inventory_item_id = request.form.get("inventory_item")
        input_name = request.form.get("input_name")
        quantity = float(request.form.get("quantity"))

        date_str = request.form.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

        notes = request.form.get("notes")

        # 🔎 Get planting
        planting = Planting.query.get(planting_id)

        # 🚫 Prevent application before planting
        if date and date < planting.planting_date:
            flash("Application date cannot be before the planting date.", "danger")
            return redirect(url_for("main.applications"))

        # Handle inventory
        if inventory_item_id:

            item = InventoryItem.query.get(inventory_item_id)

            # 🚨 Prevent negative stock
            if item.quantity < quantity:
                flash(f"Not enough {item.name} in inventory", "danger")
                return redirect(url_for("main.applications"))

            # 🔥 Deduct inventory
            item.quantity -= quantity

        application = Application(
            planting_id=planting_id,
            inventory_item_id=inventory_item_id if inventory_item_id else None,
            input_name=input_name,
            quantity=quantity,
            date=date,
            notes=notes
        )

        db.session.add(application)
        db.session.commit()

        return redirect(url_for("main.applications"))

    applications = Application.query.all()

    return render_template(
        "applications.html",
        applications=applications,
        plantings=plantings,
        inventory_items=inventory_items
    )

############# EDIT ###############

@main.route("/crops/applications/edit/<int:id>", methods=["POST"])
def edit_application(id):

    application = Application.query.get_or_404(id)

    old_quantity = application.quantity
    inventory_item_id = application.inventory_item_id

    new_quantity = float(request.form.get("quantity"))

    date_str = request.form.get("date")
    if date_str:
        application.date = datetime.strptime(date_str, "%Y-%m-%d").date()

    application.input_name = request.form.get("input_name")
    application.notes = request.form.get("notes")

    if inventory_item_id:

        item = InventoryItem.query.get(inventory_item_id)

        # Step 1: return old quantity
        item.quantity += old_quantity

        # Step 2: check if enough stock for new quantity
        if item.quantity < new_quantity:
            flash(f"Not enough {item.name} in inventory", "danger")
            return redirect(url_for("main.applications"))

        # Step 3: deduct new quantity
        item.quantity -= new_quantity

    application.quantity = new_quantity

    db.session.commit()

    return redirect(url_for("main.applications"))

########### DELETE ###############

@main.route("/crops/applications/delete/<int:id>")
def delete_application(id):

    application = Application.query.get_or_404(id)

    if application.inventory_item_id:
        item = InventoryItem.query.get(application.inventory_item_id)
        item.quantity += application.quantity

    db.session.delete(application)
    db.session.commit()

    return redirect(url_for("main.applications"))

##################################
            # HARVEST #
##################################

@main.route("/crops/harvest", methods=["GET", "POST"])
def harvest():

    plantings = Planting.query.all()

    if request.method == "POST":

        planting_id = request.form.get("planting")
        quantity = float(request.form.get("quantity"))
        unit = request.form.get("unit")

        date_str = request.form.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

        notes = request.form.get("notes")

        # 🔎 Get the planting record
        planting = Planting.query.get(planting_id)

        # 🚫 Prevent harvest before planting date
        if date and date < planting.planting_date:
            flash("Harvest date cannot be before the planting date.", "danger")
            return redirect(url_for("main.harvest"))

        harvest = Harvest(
            planting_id=planting_id,
            quantity=quantity,
            unit=unit,
            date=date,
            notes=notes
        )

        db.session.add(harvest)
        db.session.commit()

        return redirect(url_for("main.harvest"))

    harvests = Harvest.query.all()

    return render_template(
        "harvest.html",
        harvests=harvests,
        plantings=plantings
    )

################ EDIT ##################

@main.route("/crops/harvest/edit/<int:id>", methods=["POST"])
def edit_harvest(id):

    harvest = Harvest.query.get_or_404(id)

    harvest.planting_id = request.form.get("planting")
    harvest.quantity = float(request.form.get("quantity"))
    harvest.unit = request.form.get("unit")

    date_str = request.form.get("date")
    harvest.date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

    harvest.notes = request.form.get("notes")

    db.session.commit()

    return redirect(url_for("main.harvest"))


@main.route("/crops/harvest/delete/<int:id>")
def delete_harvest(id):

    harvest = Harvest.query.get_or_404(id)

    db.session.delete(harvest)
    db.session.commit()

    return redirect(url_for("main.harvest"))

   
#############################################
            #LIVESTOCK MODULE#
#############################################

@main.route("/livestock")
def livestock():
    return render_template("livestock.html")

@main.route("/finance")
def finance():
    return render_template("finance.html")

#############################################
            #REPORTS MODULE#
#############################################

@main.route("/reports")
def reports():
    return render_template("reports.html")


@main.route("/reports/crops")
def crop_reports():

    harvests = Harvest.query.all()

    return render_template(
        "crop_reports.html",
        harvests=harvests
    )
    
