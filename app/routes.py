from flask import Blueprint, render_template
from flask import request, redirect, url_for
from datetime import datetime
from .models import CropType
from .models import Field
from .models import Planting
from datetime import datetime
from . import db

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

######### DELETE #############

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

############### EDIT ##############

@main.route("/crops/plantings/edit/<int:id>", methods=["POST"])
def edit_planting(id):

    planting = Planting.query.get_or_404(id)

    planting.crop_type_id = request.form.get("crop_type")
    planting.field_id = request.form.get("field")

    planting.planting_date = request.form.get("planting_date")
    planting.expected_harvest = request.form.get("expected_harvest")

    db.session.commit()

    return redirect(url_for("main.plantings"))

############# DELETE ##############

@main.route("/crops/plantings/delete/<int:id>")
def delete_planting(id):

    planting = Planting.query.get_or_404(id)

    db.session.delete(planting)
    db.session.commit()

    return redirect(url_for("main.plantings"))


#############################################
            #LIVESTOCK MODULE#
#############################################

@main.route("/livestock")
def livestock():
    return render_template("livestock.html")

@main.route("/finance")
def finance():
    return render_template("finance.html")

@main.route("/reports")
def reports():
    return render_template("reports.html")
