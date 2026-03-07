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
from .models import AnimalType
from .models import Animal
from .models import Production
from .models import WeightRecord
from .models import AnimalExit
from .models import HealthRecord
from .models import BreedingEvent
from .models import Birth
from .models import FeedType
from .models import FeedRecord
from .models import HealthRecord
from .models import FinanceTransaction
from .models import FinanceCategory
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

    animal_types = AnimalType.query.all()

    return render_template(
        "livestock.html",
        animal_types=animal_types
    )

@main.route("/livestock/animal-types", methods=["GET", "POST"])
def animal_types():

    if request.method == "POST":

        name = request.form.get("name")
        breed = request.form.get("breed")

        animal_type = AnimalType(
            name=name,
            breed=breed
        )

        db.session.add(animal_type)
        db.session.commit()

        return redirect(url_for("main.animal_types"))

    animal_types = AnimalType.query.all()

    return render_template(
        "animal_types.html",
        animal_types=animal_types
    )

@main.route("/livestock/animal-types/edit/<int:id>", methods=["POST"])
def edit_animal_type(id):

    animal = AnimalType.query.get_or_404(id)

    animal.name = request.form.get("name")
    animal.breed = request.form.get("breed")

    db.session.commit()

    return redirect(url_for("main.animal_types"))


@main.route("/livestock/animal-types/delete/<int:id>")
def delete_animal_type(id):

    animal = AnimalType.query.get_or_404(id)

    db.session.delete(animal)
    db.session.commit()

    return redirect(url_for("main.animal_types"))


@main.route("/livestock/animals", methods=["GET", "POST"])
def animals():

    animal_types = AnimalType.query.all()

    if request.method == "POST":

        tag_number = request.form.get("tag_number")
        animal_type_id = request.form.get("animal_type")
        sex = request.form.get("sex")

        dob_str = request.form.get("date_of_birth")
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None

        notes = request.form.get("notes")
        
        purpose = request.form.get("purpose")
        quantity = request.form.get("quantity")

        animal = Animal(
            tag_number=tag_number,
            animal_type_id=animal_type_id,
            purpose=purpose,
            quantity=quantity,
            sex=sex,
            date_of_birth=dob,
            notes=notes
        )

        db.session.add(animal)
        db.session.commit()

        return redirect(url_for("main.animals"))

    animals = Animal.query.all()

    return render_template(
        "animals.html",
        animals=animals,
        animal_types=animal_types
    )

##################### EDIT ###################

@main.route("/livestock/animals/edit/<int:id>", methods=["POST"])
def edit_animal(id):

    animal = Animal.query.get_or_404(id)

    animal.tag_number = request.form.get("tag_number")
    animal.animal_type_id = request.form.get("animal_type")
    animal.sex = request.form.get("sex")

    dob_str = request.form.get("date_of_birth")
    if dob_str:
        animal.date_of_birth = datetime.strptime(dob_str, "%Y-%m-%d").date()

    animal.notes = request.form.get("notes")

    db.session.commit()

    return redirect(url_for("main.animals"))

############## DELETE #################

@main.route("/livestock/animals/delete/<int:id>")
def delete_animal(id):

    animal = Animal.query.get_or_404(id)

    db.session.delete(animal)
    db.session.commit()

    return redirect(url_for("main.animals"))

################# PRODUCTION ################

@main.route("/livestock/production", methods=["GET", "POST"])
def production():

    animals = Animal.query.filter_by(
        status="active",
        purpose="production"
    ).all()

    if request.method == "POST":

        animal_id = request.form.get("animal")
        product = request.form.get("product")
        quantity = float(request.form.get("quantity"))
        unit = request.form.get("unit")

        date_str = request.form.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

        notes = request.form.get("notes")

        new_record = Production(
            animal_id=animal_id,
            product=product,
            quantity=quantity,
            unit=unit,
            date=date,
            notes=notes
        )

        db.session.add(new_record)
        db.session.commit()

        return redirect(url_for("main.production"))

    productions = Production.query.all()

    return render_template(
        "production.html",
        productions=productions,
        animals=animals
    )

############# WEIGHT TRACK #################

@main.route("/livestock/weights", methods=["GET", "POST"])
def weight_records():

    animals = Animal.query.filter_by(status="active").all()

    if request.method == "POST":

        animal_id = request.form.get("animal")
        weight = float(request.form.get("weight"))
        unit = request.form.get("unit")

        date_str = request.form.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

        notes = request.form.get("notes")

        record = WeightRecord(
            animal_id=animal_id,
            weight=weight,
            unit=unit,
            date=date,
            notes=notes
        )

        db.session.add(record)
        db.session.commit()

        return redirect(url_for("main.weight_records"))

    weights = WeightRecord.query.all()

    return render_template(
        "weights.html",
        weights=weights,
        animals=animals
    )

############## EXITS ###################

@main.route("/livestock/exits", methods=["GET", "POST"])
def exits():

    animals = Animal.query.filter_by(status="active").all()

    if request.method == "POST":

        animal_id = request.form.get("animal")
        exit_type = request.form.get("exit_type")
        quantity = int(request.form.get("quantity"))

        date_str = request.form.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

        notes = request.form.get("notes")

        animal = Animal.query.get(animal_id)

        # prevent invalid quantities
        if quantity > animal.quantity:
            flash("Exit quantity cannot exceed current quantity", "danger")
            return redirect(url_for("main.exits"))

        exit_record = AnimalExit(
            animal_id=animal_id,
            exit_type=exit_type,
            quantity=quantity,
            date=date,
            notes=notes
        )

        # update animal quantity
        animal.quantity -= quantity

        # if individual animal
        if animal.quantity == 0:
            animal.status = exit_type

        db.session.add(exit_record)
        db.session.commit()

        return redirect(url_for("main.exits"))

    exits = AnimalExit.query.all()

    return render_template(
        "exits.html",
        exits=exits,
        animals=animals
    )
    

########### BREEDING ############

@main.route("/livestock/breeding")
def breeding():

    return render_template("breeding.html")


@main.route("/livestock/breeding/events", methods=["GET", "POST"])
def breeding_events():

    males = Animal.query.filter_by(sex="Male", status="active").all()
    females = Animal.query.filter_by(sex="Female", status="active").all()

    if request.method == "POST":

        male_id = request.form.get("male")
        female_id = request.form.get("female")

        male_breed = request.form.get("male_breed")
        female_breed = request.form.get("female_breed")

        breeding_type = request.form.get("breeding_type")

        breeding_date_str = request.form.get("breeding_date")
        breeding_date = datetime.strptime(
            breeding_date_str, "%Y-%m-%d"
        ).date() if breeding_date_str else None

        expected_birth_str = request.form.get("expected_birth")
        expected_birth = datetime.strptime(
            expected_birth_str, "%Y-%m-%d"
        ).date() if expected_birth_str else None

        notes = request.form.get("notes")

        event = BreedingEvent(
            male_id=male_id if male_id else None,
            female_id=female_id,
            male_breed=male_breed,
            female_breed=female_breed,
            breeding_type=breeding_type,
            breeding_date=breeding_date,
            expected_birth=expected_birth,
            notes=notes
        )

        db.session.add(event)
        db.session.commit()

        return redirect(url_for("main.breeding_events"))

    events = BreedingEvent.query.all()

    return render_template(
        "breeding_events.html",
        events=events,
        males=males,
        females=females
    )

########### BIRTH RECORD ###########

@main.route("/livestock/breeding/births", methods=["GET", "POST"])
def births():

    breeding_events = BreedingEvent.query.all()

    if request.method == "POST":

        breeding_event_id = request.form.get("breeding_event")

        birth_date_str = request.form.get("birth_date")
        birth_date = datetime.strptime(
            birth_date_str, "%Y-%m-%d"
        ).date() if birth_date_str else None

        offspring_breed = request.form.get("offspring_breed")

        male_offspring = int(request.form.get("male_offspring") or 0)
        female_offspring = int(request.form.get("female_offspring") or 0)

        notes = request.form.get("notes")

        record = Birth(
            breeding_event_id=breeding_event_id,
            birth_date=birth_date,
            offspring_breed=offspring_breed,
            male_offspring=male_offspring,
            female_offspring=female_offspring,
            notes=notes
        )

        db.session.add(record)
        db.session.commit()

        return redirect(url_for("main.births"))

    births = Birth.query.all()

    return render_template(
        "births.html",
        births=births,
        breeding_events=breeding_events
    )

#####################################
#           FEED RECORDS            #
#####################################

@main.route("/livestock/feed-management")
def feed_management():

    return render_template("feed_management.html")



@main.route("/livestock/feed_records", methods=["GET", "POST"])
def feed_records():

    animals = Animal.query.filter_by(status="active").all()
    feed_types = FeedType.query.all()

    if request.method == "POST":

        animal_id = request.form.get("animal")
        feed_type_id = request.form.get("feed_type")

        quantity = request.form.get("quantity")
        unit = request.form.get("unit")

        date_str = request.form.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

        notes = request.form.get("notes")

        record = FeedRecord(
            animal_id=animal_id,
            feed_type_id=feed_type_id,
            quantity=quantity,
            unit=unit,
            date=date,
            notes=notes
        )

        db.session.add(record)
        db.session.commit()

        return redirect(url_for("main.feed_records"))

    records = FeedRecord.query.order_by(FeedRecord.date.desc()).all()

    return render_template(
        "feed_records.html",
        animals=animals,
        feed_types=feed_types,
        records=records
    )

########### EDIT FEED RECORDS

@main.route("/livestock/feed-records/edit/<int:id>", methods=["POST"])
def edit_feed_record(id):

    record = FeedRecord.query.get_or_404(id)

    record.animal_id = request.form.get("animal")
    record.feed_type_id = request.form.get("feed_type")
    record.quantity = request.form.get("quantity")
    record.unit = request.form.get("unit")

    date_str = request.form.get("date")
    record.date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

    record.notes = request.form.get("notes")

    db.session.commit()

    return redirect(url_for("main.feed_records"))


@main.route("/livestock/feed-types", methods=["GET", "POST"])
def feed_types():

    if request.method == "POST":

        name = request.form.get("name")
        default_unit = request.form.get("default_unit")
        notes = request.form.get("notes")

        feed = FeedType(
            name=name,
            default_unit=default_unit,
            notes=notes
        )

        db.session.add(feed)
        db.session.commit()

        return redirect(url_for("main.feed_types"))

    feed_types = FeedType.query.all()

    return render_template(
        "feed_types.html",
        feed_types=feed_types
    )

########### EDIT FEED TYPE 

@main.route("/livestock/feed-types/edit/<int:id>", methods=["POST"])
def edit_feed_type(id):

    feed = FeedType.query.get_or_404(id)

    feed.name = request.form.get("name")
    feed.default_unit = request.form.get("default_unit")
    feed.notes = request.form.get("notes")

    db.session.commit()

    return redirect(url_for("main.feed_types"))

############ DELETE FEED TYPE

@main.route("/livestock/feed-types/delete/<int:id>")
def delete_feed_type(id):

    feed = FeedType.query.get_or_404(id)

    db.session.delete(feed)
    db.session.commit()

    return redirect(url_for("main.feed_types"))


############# HEALTH RECORDS ################

@main.route("/livestock/health-records", methods=["GET", "POST"])
def health_records():

    animals = Animal.query.filter_by(status="active").all()

    if request.method == "POST":

        animal_id = request.form.get("animal")
        condition = request.form.get("condition")
        treatment = request.form.get("treatment")
        medication = request.form.get("medication")

        date_str = request.form.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

        notes = request.form.get("notes")

        record = HealthRecord(
            animal_id=animal_id,
            condition=condition,
            treatment=treatment,
            medication=medication,
            date=date,
            notes=notes
        )

        db.session.add(record)
        db.session.commit()

        return redirect(url_for("main.health_records"))

    records = HealthRecord.query.order_by(HealthRecord.date.desc()).all()

    return render_template(
        "health_records.html",
        animals=animals,
        records=records
    )

############# EDIT HEALTH RECORDS

@main.route("/livestock/health-records/edit/<int:id>", methods=["POST"])
def edit_health_record(id):

    record = HealthRecord.query.get_or_404(id)

    record.animal_id = request.form.get("animal")
    record.condition = request.form.get("condition")
    record.treatment = request.form.get("treatment")
    record.medication = request.form.get("medication")

    date_str = request.form.get("date")
    record.date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

    record.notes = request.form.get("notes")

    db.session.commit()

    return redirect(url_for("main.health_records"))



########################
#       FINANCE        #
########################

@main.route("/finance")
def finance():
    return render_template("finance.html")


########## TRANSACTIONS

@main.route("/finance/transactions", methods=["GET", "POST"])
def finance_transactions():

    categories = FinanceCategory.query.all()

    if request.method == "POST":

        type = request.form.get("type")
        category_id = request.form.get("category")
        description = request.form.get("description")
        amount = request.form.get("amount")
        date = request.form.get("date")
        notes = request.form.get("notes")

        # Basic validation
        if not type or not category_id or not amount or not date:
            return redirect(url_for("main.finance_transactions"))

        transaction = FinanceTransaction(
            type=type,
            category_id=category_id,
            description=description,
            amount=amount,
            date=date,
            notes=notes
        )

        db.session.add(transaction)
        db.session.commit()

        return redirect(url_for("main.finance_transactions"))

    transactions = FinanceTransaction.query.order_by(
        FinanceTransaction.date.desc()
    ).all()

    return render_template(
        "finance_transactions.html",
        transactions=transactions,
        categories=categories
    )
    
########### FINANCE CATEGORIES

@main.route("/finance/categories", methods=["GET", "POST"])
def finance_categories():

    if request.method == "POST":

        name = request.form.get("name")
        type = request.form.get("type")
        description = request.form.get("description")

        category = FinanceCategory(
            name=name,
            type=type,
            description=description
        )

        db.session.add(category)
        db.session.commit()

        return redirect(url_for("main.finance_categories"))

    categories = FinanceCategory.query.order_by(
        FinanceCategory.type
    ).all()

    return render_template(
        "finance_categories.html",
        categories=categories
    )
    
############# EDIT CATEGORY

@main.route("/finance/categories/edit/<int:id>", methods=["POST"])
def edit_finance_category(id):

    category = FinanceCategory.query.get_or_404(id)

    category.name = request.form.get("name")
    category.type = request.form.get("type")
    category.description = request.form.get("description")

    db.session.commit()

    return redirect(url_for("main.finance_categories"))


############# DELETE CATEGORY

@main.route("/finance/categories/delete/<int:id>")
def delete_finance_category(id):

    category = FinanceCategory.query.get_or_404(id)

    db.session.delete(category)
    db.session.commit()

    return redirect(url_for("main.finance_categories"))



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
    
