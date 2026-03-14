from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from . import main
from .. import db
from ..models import CropType, Field, Planting, InventoryItem, Application, Harvest
from flask_login import login_required

################################################
# CROPS DASHBOARD
################################################

@main.route("/crops")
@login_required
def crops():
    return render_template("crops/crops.html")

################################################
# CROP TYPES (CONFIGURATION)
################################################

@main.route("/crops/types", methods=["GET", "POST"])
@login_required
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

    return render_template(
        "crops/crop_types.html",
        crops=crops
    )

# EDIT CROP TYPE
@main.route("/crops/types/edit/<int:id>", methods=["POST"])
@login_required
def edit_crop_type(id):

    crop = CropType.query.get_or_404(id)

    crop.name = request.form.get("name")
    crop.variety = request.form.get("variety")
    crop.notes = request.form.get("notes")

    db.session.commit()

    return redirect(url_for("main.crop_types"))

# DELETE CROP TYPE
@main.route("/crops/types/delete/<int:id>")
@login_required
def delete_crop_type(id):

    crop = CropType.query.get_or_404(id)

    db.session.delete(crop)
    db.session.commit()

    return redirect(url_for("main.crop_types"))

################################################
# FIELDS (CONFIGURATION)
################################################

@main.route("/crops/fields", methods=["GET", "POST"])
@login_required
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

    return render_template(
        "crops/fields.html",
        fields=fields
    )

# EDIT FIELD
@main.route("/crops/fields/edit/<int:id>", methods=["POST"])
@login_required
def edit_field(id):

    field = Field.query.get_or_404(id)

    field.name = request.form.get("name")
    field.size = request.form.get("size")
    field.location = request.form.get("location")

    db.session.commit()

    return redirect(url_for("main.fields"))

# DELETE FIELD
@main.route("/crops/fields/delete/<int:id>")
@login_required
def delete_field(id):

    field = Field.query.get_or_404(id)

    db.session.delete(field)
    db.session.commit()

    return redirect(url_for("main.fields"))

################################################
# PLANTINGS
################################################

@main.route("/crops/plantings", methods=["GET", "POST"])
@login_required
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

        existing = Planting.query.filter_by(
            field_id=field_id,
            status="active"
        ).first()

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
        "crops/plantings.html",
        plantings=plantings,
        crops=crops,
        fields=fields
    )

# COMPLETE PLANTING
@main.route("/crops/plantings/complete/<int:id>")
@login_required
def complete_planting(id):

    planting = Planting.query.get_or_404(id)

    planting.status = "completed"

    db.session.commit()

    flash("Planting marked as completed.", "success")

    return redirect(url_for("main.plantings"))

################################################
# INPUT APPLICATIONS
################################################

@main.route("/crops/applications", methods=["GET", "POST"])
@login_required
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

        planting = Planting.query.get(planting_id)

        if date and date < planting.planting_date:
            flash("Application date cannot be before the planting date.", "danger")
            return redirect(url_for("main.applications"))

        if inventory_item_id:

            item = InventoryItem.query.get(inventory_item_id)

            if item.quantity < quantity:
                flash(f"Not enough {item.name} in inventory", "danger")
                return redirect(url_for("main.applications"))

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
        "crops/applications.html",
        applications=applications,
        plantings=plantings,
        inventory_items=inventory_items
    )

# EDIT APPLICATION
@main.route("/crops/applications/edit/<int:id>", methods=["POST"])
@login_required
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

        item.quantity += old_quantity

        if item.quantity < new_quantity:
            flash(f"Not enough {item.name} in inventory", "danger")
            return redirect(url_for("main.applications"))

        item.quantity -= new_quantity

    application.quantity = new_quantity

    db.session.commit()

    return redirect(url_for("main.applications"))

################################################
# HARVEST
################################################

@main.route("/crops/harvest", methods=["GET", "POST"])
@login_required
def harvest():

    plantings = Planting.query.all()

    if request.method == "POST":

        planting_id = request.form.get("planting")
        quantity = float(request.form.get("quantity"))
        unit = request.form.get("unit")

        date_str = request.form.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

        notes = request.form.get("notes")

        planting = Planting.query.get(planting_id)

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
        "crops/harvest.html",
        harvests=harvests,
        plantings=plantings
    )

# EDIT HARVEST
@main.route("/crops/harvest/edit/<int:id>", methods=["POST"])
@login_required
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