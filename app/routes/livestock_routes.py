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

    ################################################
    # ADD ANIMAL
    ################################################

    if request.method == "POST":

        tag_number = request.form.get("tag_number")
        animal_type_id = request.form.get("animal_type")
        sex = request.form.get("sex")
        purpose = request.form.get("purpose")
        quantity = request.form.get("quantity")

        dob_str = request.form.get("date_of_birth")

        dob = (
            datetime.strptime(dob_str, "%Y-%m-%d").date()
            if dob_str else None
        )

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

        flash("Animal added successfully.", "success")

        return redirect(url_for("main.animals"))

    ################################################
    # SEARCH + PAGINATION
    ################################################

    search = request.args.get("search", "")

    query = Animal.query

    if search:

        query = query.filter(
            Animal.tag_number.ilike(f"%{search}%")
        )

    page = request.args.get("page", 1, type=int)

    animals = query.order_by(
        Animal.id.desc()
    ).paginate(
        page=page,
        per_page=20
    )

    ################################################
    # QUICK STATS
    ################################################

    active_count = Animal.query.filter_by(
        status="active"
    ).count()

    ################################################
    # RENDER TEMPLATE
    ################################################

    return render_template(
        "livestock/animals.html",
        animals=animals,
        animal_types=animal_types,
        active_count=active_count
    )

# EDIT ANIMAL 

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

    ################################################
    # LOAD ACTIVE PRODUCTION ANIMALS
    ################################################

    animals = Animal.query.filter_by(
        status="active",
        purpose="production"
    ).all()

    ################################################
    # ADD PRODUCTION RECORD
    ################################################

    if request.method == "POST":

        animal_id = request.form.get("animal")

        product = request.form.get("product")

        quantity = float(
            request.form.get("quantity") or 0
        )

        unit = request.form.get("unit")

        ################################################
        # DATE
        ################################################

        date_str = request.form.get("date")

        date = (
            datetime.strptime(
                date_str,
                "%Y-%m-%d"
            ).date()
            if date_str else None
        )

        ################################################
        # NOTES
        ################################################

        notes = request.form.get("notes")

        ################################################
        # SAVE RECORD
        ################################################

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

        flash(
            "Production record added successfully.",
            "success"
        )

        return redirect(
            url_for("main.production")
        )

    ################################################
    # SEARCH + PAGINATION
    ################################################

    search = request.args.get("search", "")

    query = Production.query

    if search:

        query = query.join(
            Animal,
            Production.animal_id == Animal.id
        ).filter(
            Animal.tag_number.ilike(f"%{search}%")
        )

    ################################################
    # PAGINATION
    ################################################

    page = request.args.get(
        "page",
        1,
        type=int
    )

    productions = query.order_by(
        Production.date.desc()
    ).paginate(
        page=page,
        per_page=20
    )

    ################################################
    # QUICK STATS
    ################################################

    total_records = Production.query.count()

    total_quantity = db.session.query(
        db.func.sum(Production.quantity)
    ).scalar() or 0

    ################################################
    # RENDER TEMPLATE
    ################################################

    return render_template(
        "livestock/production.html",
        productions=productions,
        animals=animals,
        total_records=total_records,
        total_quantity=total_quantity
    )


################################################
# EDIT PRODUCTION RECORD
################################################

@main.route(
    "/livestock/production/edit/<int:id>",
    methods=["POST"]
)
def edit_production(id):

    production = Production.query.get_or_404(id)

    ################################################
    # UPDATE FIELDS
    ################################################

    production.product = request.form.get("product")

    production.quantity = float(
        request.form.get("quantity") or 0
    )

    production.unit = request.form.get("unit")

    ################################################
    # DATE
    ################################################

    date_str = request.form.get("date")

    production.date = (
        datetime.strptime(
            date_str,
            "%Y-%m-%d"
        ).date()
        if date_str else None
    )

    ################################################
    # NOTES
    ################################################

    production.notes = request.form.get("notes")

    db.session.commit()

    flash(
        "Production record updated successfully.",
        "success"
    )

    return redirect(
        url_for("main.production")
    )


################################################
# WEIGHT RECORDS
################################################

@main.route("/livestock/weights", methods=["GET", "POST"])
def weight_records():

    ################################################
    # LOAD ACTIVE ANIMALS
    ################################################

    animals = Animal.query.filter_by(
        status="active"
    ).all()

    ################################################
    # ADD WEIGHT RECORD
    ################################################

    if request.method == "POST":

        animal_id = request.form.get("animal")

        weight = float(
            request.form.get("weight") or 0
        )

        unit = request.form.get("unit")

        ################################################
        # DATE
        ################################################

        date_str = request.form.get("date")

        date = (
            datetime.strptime(
                date_str,
                "%Y-%m-%d"
            ).date()
            if date_str else None
        )

        ################################################
        # NOTES
        ################################################

        notes = request.form.get("notes")

        ################################################
        # SAVE RECORD
        ################################################

        record = WeightRecord(
            animal_id=animal_id,
            weight=weight,
            unit=unit,
            date=date,
            notes=notes
        )

        db.session.add(record)
        db.session.commit()

        flash(
            "Weight record added successfully.",
            "success"
        )

        return redirect(
            url_for("main.weight_records")
        )

    ################################################
    # SEARCH + PAGINATION
    ################################################

    search = request.args.get("search", "")

    query = WeightRecord.query

    if search:

        query = query.join(
            Animal,
            WeightRecord.animal_id == Animal.id
        ).filter(
            Animal.tag_number.ilike(f"%{search}%")
        )

    ################################################
    # PAGINATION
    ################################################

    page = request.args.get(
        "page",
        1,
        type=int
    )

    weights = query.order_by(
        WeightRecord.date.desc()
    ).paginate(
        page=page,
        per_page=20
    )

    ################################################
    # QUICK STATS
    ################################################

    total_records = WeightRecord.query.count()

    average_weight = db.session.query(
        db.func.avg(WeightRecord.weight)
    ).scalar()

    average_weight = round(
        average_weight,
        2
    ) if average_weight else 0

    ################################################
    # RENDER TEMPLATE
    ################################################

    return render_template(
        "livestock/weights.html",
        weights=weights,
        animals=animals,
        total_records=total_records,
        average_weight=average_weight
    )


################################################
# EDIT WEIGHT RECORD
################################################

@main.route(
    "/livestock/weights/edit/<int:id>",
    methods=["POST"]
)
def edit_weight(id):

    weight_record = WeightRecord.query.get_or_404(id)

    ################################################
    # UPDATE FIELDS
    ################################################

    weight_record.weight = float(
        request.form.get("weight") or 0
    )

    weight_record.unit = request.form.get("unit")

    ################################################
    # DATE
    ################################################

    date_str = request.form.get("date")

    weight_record.date = (
        datetime.strptime(
            date_str,
            "%Y-%m-%d"
        ).date()
        if date_str else None
    )

    ################################################
    # NOTES
    ################################################

    weight_record.notes = request.form.get("notes")

    db.session.commit()

    flash(
        "Weight record updated successfully.",
        "success"
    )

    return redirect(
        url_for("main.weight_records")
    )

################################################
# ANIMAL EXITS
################################################

@main.route("/livestock/exits", methods=["GET", "POST"])
def exits():

    ################################################
    # LOAD ACTIVE ANIMALS
    ################################################

    animals = Animal.query.filter_by(
        status="active"
    ).all()

    ################################################
    # ADD EXIT RECORD
    ################################################

    if request.method == "POST":

        animal_id = request.form.get("animal")
        exit_type = request.form.get("exit_type")

        quantity = int(
            request.form.get("quantity") or 0
        )

        date_str = request.form.get("date")

        date = (
            datetime.strptime(
                date_str,
                "%Y-%m-%d"
            ).date()
            if date_str else None
        )

        notes = request.form.get("notes")

        animal = Animal.query.get(animal_id)

        ################################################
        # VALIDATION
        ################################################

        if not animal:

            flash("Animal not found.", "danger")

            return redirect(url_for("main.exits"))

        if quantity <= 0:

            flash("Quantity must be greater than 0.", "danger")

            return redirect(url_for("main.exits"))

        if quantity > animal.quantity:

            flash(
                "Exit quantity cannot exceed current quantity.",
                "danger"
            )

            return redirect(url_for("main.exits"))

        ################################################
        # CREATE EXIT RECORD
        ################################################

        exit_record = AnimalExit(
            animal_id=animal_id,
            exit_type=exit_type,
            quantity=quantity,
            date=date,
            notes=notes
        )

        ################################################
        # UPDATE ANIMAL QUANTITY
        ################################################

        animal.quantity -= quantity

        if animal.quantity == 0:

            animal.status = exit_type

        db.session.add(exit_record)
        db.session.commit()

        flash("Exit record added successfully.", "success")

        return redirect(url_for("main.exits"))

    ################################################
    # SEARCH + PAGINATION
    ################################################

    search = request.args.get("search", "")

    query = AnimalExit.query

    if search:

        query = query.join(
            Animal,
            AnimalExit.animal_id == Animal.id
        ).filter(
            Animal.tag_number.ilike(f"%{search}%")
        )

    page = request.args.get("page", 1, type=int)

    exits = query.order_by(
        AnimalExit.id.desc()
    ).paginate(
        page=page,
        per_page=20
    )

    ################################################
    # QUICK STATS
    ################################################

    total_exits = AnimalExit.query.count()

    total_quantity = db.session.query(
        db.func.sum(AnimalExit.quantity)
    ).scalar() or 0

    ################################################
    # RENDER TEMPLATE
    ################################################

    return render_template(
        "livestock/exits.html",
        exits=exits,
        animals=animals,
        total_exits=total_exits,
        total_quantity=total_quantity
    )


################################################
# EDIT EXIT RECORD
################################################

@main.route("/livestock/exits/edit/<int:id>", methods=["POST"])
def edit_exit(id):

    record = AnimalExit.query.get_or_404(id)

    record.exit_type = request.form.get("exit_type")

    record.quantity = int(
        request.form.get("quantity") or 1
    )

    date_str = request.form.get("date")

    record.date = (
        datetime.strptime(
            date_str,
            "%Y-%m-%d"
        ).date()
        if date_str else None
    )

    record.notes = request.form.get("notes")

    db.session.commit()

    flash("Exit record updated successfully.", "success")

    return redirect(url_for("main.exits"))
    
################################################
# BREEDING
################################################

@main.route("/livestock/breeding")
def breeding():

    breeding_events_count = BreedingEvent.query.count()
    births_count = Birth.query.count()

    return render_template(
        "livestock/breeding.html",
        breeding_events_count=breeding_events_count,
        births_count=births_count
    )


################################################
# BREEDING EVENTS
################################################

@main.route("/livestock/breeding/events", methods=["GET", "POST"])
def breeding_events():

    ################################################
    # LOAD ANIMALS
    ################################################

    males = Animal.query.filter_by(
        sex="Male",
        status="active"
    ).all()

    females = Animal.query.filter_by(
        sex="Female",
        status="active"
    ).all()

    ################################################
    # ADD BREEDING EVENT
    ################################################

    if request.method == "POST":

        male_id = request.form.get("male")
        female_id = request.form.get("female")

        male_breed = request.form.get("male_breed")
        female_breed = request.form.get("female_breed")

        breeding_type = request.form.get("breeding_type")

        breeding_date_str = request.form.get("breeding_date")

        breeding_date = (
            datetime.strptime(
                breeding_date_str,
                "%Y-%m-%d"
            ).date()
            if breeding_date_str else None
        )

        expected_birth_str = request.form.get("expected_birth")

        expected_birth = (
            datetime.strptime(
                expected_birth_str,
                "%Y-%m-%d"
            ).date()
            if expected_birth_str else None
        )

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

        flash("Breeding event recorded successfully.", "success")

        return redirect(url_for("main.breeding_events"))

    ################################################
    # SEARCH + PAGINATION
    ################################################

    search = request.args.get("search", "")

    query = BreedingEvent.query

    if search:

        query = query.join(
            Animal,
            BreedingEvent.female_id == Animal.id
        ).filter(
            Animal.tag_number.ilike(f"%{search}%")
        )

    page = request.args.get("page", 1, type=int)

    events = query.order_by(
        BreedingEvent.id.desc()
    ).paginate(
        page=page,
        per_page=20
    )

    ################################################
    # QUICK STATS
    ################################################

    pending_count = BreedingEvent.query.filter(
        BreedingEvent.expected_birth.isnot(None)
    ).count()

    ################################################
    # RENDER TEMPLATE
    ################################################

    return render_template(
        "livestock/breeding_events.html",
        events=events,
        males=males,
        females=females,
        pending_count=pending_count
    )


################################################
# EDIT BREEDING EVENT
################################################

@main.route(
    "/livestock/breeding/events/edit/<int:id>",
    methods=["POST"]
)
def edit_breeding_event(id):

    event = BreedingEvent.query.get_or_404(id)

    breeding_date_str = request.form.get("breeding_date")

    if breeding_date_str:

        event.breeding_date = datetime.strptime(
            breeding_date_str,
            "%Y-%m-%d"
        ).date()

    expected_birth_str = request.form.get("expected_birth")

    if expected_birth_str:

        event.expected_birth = datetime.strptime(
            expected_birth_str,
            "%Y-%m-%d"
        ).date()

    else:

        event.expected_birth = None

    event.notes = request.form.get("notes")

    db.session.commit()

    flash("Breeding event updated successfully.", "success")

    return redirect(url_for("main.breeding_events"))
################################################
# BIRTH RECORDS
################################################

@main.route("/livestock/breeding/births", methods=["GET", "POST"])
def births():

    ################################################
    # LOAD BREEDING EVENTS
    ################################################

    breeding_events = BreedingEvent.query.order_by(
        BreedingEvent.id.desc()
    ).all()

    ################################################
    # ADD BIRTH RECORD
    ################################################

    if request.method == "POST":

        breeding_event_id = request.form.get("breeding_event")

        if not breeding_event_id:

            flash("Please select a breeding event.", "danger")

            return redirect(url_for("main.births"))

        birth_date_str = request.form.get("birth_date")

        birth_date = (
            datetime.strptime(
                birth_date_str,
                "%Y-%m-%d"
            ).date()
            if birth_date_str else None
        )

        offspring_breed = request.form.get("offspring_breed")

        male_offspring = int(
            request.form.get("male_offspring") or 0
        )

        female_offspring = int(
            request.form.get("female_offspring") or 0
        )

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

        flash("Birth record added successfully.", "success")

        return redirect(url_for("main.births"))

    ################################################
    # SEARCH + PAGINATION
    ################################################

    search = request.args.get("search", "")

    query = Birth.query

    if search:

        query = query.join(
            BreedingEvent,
            Birth.breeding_event_id == BreedingEvent.id
        ).join(
            Animal,
            BreedingEvent.female_id == Animal.id
        ).filter(
            Animal.tag_number.ilike(f"%{search}%")
        )

    page = request.args.get("page", 1, type=int)

    births = query.order_by(
        Birth.id.desc()
    ).paginate(
        page=page,
        per_page=20
    )

    ################################################
    # QUICK STATS
    ################################################

    total_births = Birth.query.count()

    total_offspring = db.session.query(
        db.func.sum(Birth.male_offspring + Birth.female_offspring)
    ).scalar() or 0

    ################################################
    # RENDER TEMPLATE
    ################################################

    return render_template(
        "livestock/births.html",
        births=births,
        breeding_events=breeding_events,
        total_births=total_births,
        total_offspring=total_offspring
    )
################################################
# FEED MANAGEMENT
################################################

@main.route("/livestock/feed-management")
def feed_management():

    return render_template(
        "livestock/feed_management.html"
    )


################################################
# FEED RECORDS
################################################

@main.route("/livestock/feed-records", methods=["GET", "POST"])
def feed_records():

    ################################################
    # LOAD DATA
    ################################################

    animals = Animal.query.filter_by(
        status="active"
    ).all()

    feed_types = FeedType.query.all()

    ################################################
    # ADD FEED RECORD
    ################################################

    if request.method == "POST":

        animal_id = request.form.get("animal")
        feed_type_id = request.form.get("feed_type")

        quantity = request.form.get("quantity")
        unit = request.form.get("unit")

        date_str = request.form.get("date")

        date = (
            datetime.strptime(
                date_str,
                "%Y-%m-%d"
            ).date()
            if date_str else None
        )

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

        flash("Feed record added successfully.", "success")

        return redirect(url_for("main.feed_records"))

    ################################################
    # SEARCH + PAGINATION
    ################################################

    search = request.args.get("search", "")

    query = FeedRecord.query

    if search:

        query = query.join(
            Animal,
            FeedRecord.animal_id == Animal.id
        ).filter(
            Animal.tag_number.ilike(f"%{search}%")
        )

    page = request.args.get("page", 1, type=int)

    records = query.order_by(
        FeedRecord.date.desc()
    ).paginate(
        page=page,
        per_page=20
    )

    ################################################
    # QUICK STATS
    ################################################

    total_records = FeedRecord.query.count()

    total_quantity = db.session.query(
        db.func.sum(FeedRecord.quantity)
    ).scalar() or 0

    ################################################
    # RENDER TEMPLATE
    ################################################

    return render_template(
        "livestock/feed_records.html",
        animals=animals,
        feed_types=feed_types,
        records=records,
        total_records=total_records,
        total_quantity=total_quantity
    )


################################################
# EDIT FEED RECORD
################################################

@main.route(
    "/livestock/feed-records/edit/<int:id>",
    methods=["POST"]
)
def edit_feed_record(id):

    record = FeedRecord.query.get_or_404(id)

    record.animal_id = request.form.get("animal")

    record.feed_type_id = request.form.get("feed_type")

    record.quantity = request.form.get("quantity")

    record.unit = request.form.get("unit")

    ################################################
    # DATE
    ################################################

    date_str = request.form.get("date")

    record.date = (
        datetime.strptime(
            date_str,
            "%Y-%m-%d"
        ).date()
        if date_str else None
    )

    ################################################
    # NOTES
    ################################################

    record.notes = request.form.get("notes")

    db.session.commit()

    flash("Feed record updated successfully.", "success")

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
    
#################
# FEED TYPES
#################

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

    ################################################
    # LOAD ACTIVE ANIMALS
    ################################################

    animals = Animal.query.filter_by(
        status="active"
    ).all()

    ################################################
    # ADD HEALTH RECORD
    ################################################

    if request.method == "POST":

        animal_id = request.form.get("animal")

        condition = request.form.get("condition")
        treatment = request.form.get("treatment")
        medication = request.form.get("medication")

        date_str = request.form.get("date")

        date = (
            datetime.strptime(
                date_str,
                "%Y-%m-%d"
            ).date()
            if date_str else None
        )

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

        flash(
            "Health record added successfully.",
            "success"
        )

        return redirect(
            url_for("main.health_records")
        )

    ################################################
    # SEARCH + PAGINATION
    ################################################

    search = request.args.get("search", "")

    query = HealthRecord.query

    if search:

        query = query.join(
            Animal,
            HealthRecord.animal_id == Animal.id
        ).filter(
            Animal.tag_number.ilike(f"%{search}%")
        )

    page = request.args.get(
        "page",
        1,
        type=int
    )

    records = query.order_by(
        HealthRecord.date.desc()
    ).paginate(
        page=page,
        per_page=20
    )

    ################################################
    # QUICK STATS
    ################################################

    total_records = HealthRecord.query.count()

    treatment_count = HealthRecord.query.filter(
        HealthRecord.treatment.isnot(None)
    ).count()

    ################################################
    # RENDER TEMPLATE
    ################################################

    return render_template(
        "livestock/health_records.html",
        animals=animals,
        records=records,
        total_records=total_records,
        treatment_count=treatment_count
    )


################################################
# EDIT HEALTH RECORD
################################################

@main.route(
    "/livestock/health-records/edit/<int:id>",
    methods=["POST"]
)
def edit_health_record(id):

    record = HealthRecord.query.get_or_404(id)

    ################################################
    # UPDATE FIELDS
    ################################################

    record.animal_id = request.form.get("animal")

    record.condition = request.form.get("condition")

    record.treatment = request.form.get("treatment")

    record.medication = request.form.get("medication")

    ################################################
    # DATE
    ################################################

    date_str = request.form.get("date")

    record.date = (
        datetime.strptime(
            date_str,
            "%Y-%m-%d"
        ).date()
        if date_str else None
    )

    ################################################
    # NOTES
    ################################################

    record.notes = request.form.get("notes")

    db.session.commit()

    flash(
        "Health record updated successfully.",
        "success"
    )

    return redirect(
        url_for("main.health_records")
    )
   