from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from . import main
from .. import db
from ..models import (
    AnimalType, Animal, Production, WeightRecord, AnimalExit,
    BreedingEvent, Birth, FeedType, FeedRecord, HealthRecord
)


################################################
# LIVESTOCK DASHBOARD
################################################

@main.route("/livestock")
def livestock():

    animal_types = AnimalType.query.all()

    return render_template(
        "livestock/livestock.html",
        animal_types=animal_types
    )


################################################
# ANIMAL TYPES (CONFIGURATION)
################################################

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
        "livestock/animal_types.html",
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


################################################
# ANIMALS
################################################

@main.route("/livestock/animals", methods=["GET", "POST"])
def animals():

    animal_types = AnimalType.query.all()

    if request.method == "POST":

        tag_number = request.form.get("tag_number")
        animal_type_id = request.form.get("animal_type")
        sex = request.form.get("sex")
        purpose = request.form.get("purpose")
        quantity = request.form.get("quantity")

        dob_str = request.form.get("date_of_birth")
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None

        notes = request.form.get("notes")

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
        "livestock/animals.html",
        animals=animals,
        animal_types=animal_types
    )


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


################################################
# PRODUCTION RECORDS
################################################

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

        record = Production(
            animal_id=animal_id,
            product=product,
            quantity=quantity,
            unit=unit,
            date=date,
            notes=notes
        )

        db.session.add(record)
        db.session.commit()

        return redirect(url_for("main.production"))

    productions = Production.query.all()

    return render_template(
        "livestock/production.html",
        productions=productions,
        animals=animals
    )


################################################
# WEIGHT RECORDS
################################################

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
        "livestock/weights.html",
        weights=weights,
        animals=animals
    )


################################################
# ANIMAL EXITS
################################################

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

        animal.quantity -= quantity

        if animal.quantity == 0:
            animal.status = exit_type

        db.session.add(exit_record)
        db.session.commit()

        return redirect(url_for("main.exits"))

    exits = AnimalExit.query.all()

    return render_template(
        "livestock/exits.html",
        exits=exits,
        animals=animals
    )
    
    ################################################
# BREEDING
################################################

@main.route("/livestock/breeding")
def breeding():
    return render_template("livestock/breeding.html")


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
        "livestock/breeding_events.html",
        events=events,
        males=males,
        females=females
    )


@main.route("/livestock/breeding/events/edit/<int:id>", methods=["POST"])
def edit_breeding_event(id):

    event = BreedingEvent.query.get_or_404(id)

    event.breeding_date = request.form.get("breeding_date")
    event.expected_birth = request.form.get("expected_birth")
    event.notes = request.form.get("notes")

    db.session.commit()

    return redirect(url_for("main.breeding_events"))

################################################
# BIRTH RECORDS
################################################

@main.route("/livestock/breeding/births", methods=["GET", "POST"])
def births():

    breeding_events = BreedingEvent.query.all()

    if request.method == "POST":

        breeding_event_id = request.form.get("breeding_event")

        if not breeding_event_id:
            return redirect(url_for("main.births"))

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
        "livestock/births.html",
        births=births,
        breeding_events=breeding_events
    )
    
################################################
# FEED MANAGEMENT
################################################

@main.route("/livestock/feed-management")
def feed_management():
    return render_template("livestock/feed_management.html")


@main.route("/livestock/feed-records", methods=["GET", "POST"])
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

    records = FeedRecord.query.order_by(
        FeedRecord.date.desc()
    ).all()

    return render_template(
        "livestock/feed_records.html",
        animals=animals,
        feed_types=feed_types,
        records=records
    )


@main.route("/livestock/feed-records/edit/<int:id>", methods=["POST"])
def edit_feed_record(id):

    record = FeedRecord.query.get_or_404(id)

    record.animal_id = request.form.get("animal")
    record.feed_type_id = request.form.get("feed_type")
    record.quantity = request.form.get("quantity")
    record.unit = request.form.get("unit")

    date_str = request.form.get("date")
    record.date = datetime.strptime(
        date_str, "%Y-%m-%d"
    ).date() if date_str else None

    record.notes = request.form.get("notes")

    db.session.commit()

    return redirect(url_for("main.feed_records"))


################################################
# FEED TYPES
################################################

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
        "livestock/feed_types.html",
        feed_types=feed_types
    )


@main.route("/livestock/feed-types/edit/<int:id>", methods=["POST"])
def edit_feed_type(id):

    feed = FeedType.query.get_or_404(id)

    feed.name = request.form.get("name")
    feed.default_unit = request.form.get("default_unit")
    feed.notes = request.form.get("notes")

    db.session.commit()

    return redirect(url_for("main.feed_types"))


@main.route("/livestock/feed-types/delete/<int:id>")
def delete_feed_type(id):

    feed = FeedType.query.get_or_404(id)

    db.session.delete(feed)
    db.session.commit()

    return redirect(url_for("main.feed_types"))


################################################
# HEALTH RECORDS
################################################

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

    records = HealthRecord.query.order_by(
        HealthRecord.date.desc()
    ).all()

    return render_template(
        "livestock/health_records.html",
        animals=animals,
        records=records
    )


@main.route("/livestock/health-records/edit/<int:id>", methods=["POST"])
def edit_health_record(id):

    record = HealthRecord.query.get_or_404(id)

    record.animal_id = request.form.get("animal")
    record.condition = request.form.get("condition")
    record.treatment = request.form.get("treatment")
    record.medication = request.form.get("medication")

    date_str = request.form.get("date")
    record.date = datetime.strptime(
        date_str, "%Y-%m-%d"
    ).date() if date_str else None

    record.notes = request.form.get("notes")

    db.session.commit()

    return redirect(url_for("main.health_records"))
   