from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class CropType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    variety = db.Column(db.String(100))
    notes = db.Column(db.Text)

    def __repr__(self):
        return f"<CropType {self.name}>"

class Field(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Float)
    location = db.Column(db.String(200))

    def __repr__(self):
        return f"<Field {self.name}>"

############# PLANTING

class Planting(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    crop_type_id = db.Column(
        db.Integer,
        db.ForeignKey('crop_type.id'),
        nullable=False
    )

    field_id = db.Column(
        db.Integer,
        db.ForeignKey('field.id'),
        nullable=False
    )

    planting_date = db.Column(db.Date)
    expected_harvest = db.Column(db.Date)

    # NEW COLUMN
    status = db.Column(db.String(20), default="active")

    crop_type = db.relationship('CropType')
    field = db.relationship('Field')

    def __repr__(self):
        return f"<Planting {self.id}>"
    
############ APPLICATION

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    planting_id = db.Column(
        db.Integer,
        db.ForeignKey('planting.id'),
        nullable=False
    )

    inventory_item_id = db.Column(
        db.Integer,
        db.ForeignKey('inventory_item.id'),
        nullable=True
    )

    date = db.Column(db.Date)

    input_name = db.Column(db.String(200))

    quantity = db.Column(db.Float)
    unit = db.Column(db.String(50))   # 👈 add this

    notes = db.Column(db.Text)

    planting = db.relationship('Planting')
    inventory_item = db.relationship('InventoryItem')

def __repr__(self):
    if self.inventory_item:
        return f"<Application {self.inventory_item.name}>"
    return f"<Application {self.input_name}>"

############### INVENTORY

class InventoryCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<InventoryCategory {self.name}>"

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('inventory_category.id')
    )

    quantity = db.Column(db.Float)
    unit = db.Column(db.String(50))

    category = db.relationship('InventoryCategory')

    def __repr__(self):
        return f"<InventoryItem {self.name}>"

################# HARVEST

class Harvest(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    planting_id = db.Column(
        db.Integer,
        db.ForeignKey('planting.id'),
        nullable=False
    )

    date = db.Column(db.Date)

    quantity = db.Column(db.Float)

    unit = db.Column(db.String(50))

    notes = db.Column(db.Text)

    planting = db.relationship('Planting')

    def __repr__(self):
        return f"<Harvest {self.quantity} {self.unit}>"


##############################
######## LIVESTOCK ###########
##############################

class AnimalType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100))

    def __repr__(self):
        return f"<AnimalType {self.name}>"


class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    tag_number = db.Column(db.String(50))

    animal_type_id = db.Column(
        db.Integer,
        db.ForeignKey('animal_type.id'),
        nullable=False
    )

    purpose = db.Column(db.String(20))   # production, breeding, meat, sale

    quantity = db.Column(db.Integer, default=1)  # supports batch animals

    sex = db.Column(db.String(10))
    date_of_birth = db.Column(db.Date)

    status = db.Column(db.String(20), default="active")

    notes = db.Column(db.Text)

    animal_type = db.relationship('AnimalType')

    def __repr__(self):
        return f"<Animal {self.tag_number}>"

class Production(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    animal_id = db.Column(
        db.Integer,
        db.ForeignKey('animal.id'),
        nullable=False
    )

    product = db.Column(db.String(50))  # Milk, Eggs, Honey
    quantity = db.Column(db.Float)
    unit = db.Column(db.String(20))     # Litres, Eggs, Kg

    date = db.Column(db.Date)

    notes = db.Column(db.Text)

    animal = db.relationship('Animal')

    def __repr__(self):
        return f"<Production {self.product}>"


class WeightRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    animal_id = db.Column(
        db.Integer,
        db.ForeignKey('animal.id'),
        nullable=False
    )

    weight = db.Column(db.Float)  # weight value
    unit = db.Column(db.String(20))  # kg, g etc

    date = db.Column(db.Date)

    notes = db.Column(db.Text)

    animal = db.relationship('Animal')

    def __repr__(self):
        return f"<WeightRecord {self.weight}>"


##################################
############ EXITS ###############
##################################

class AnimalExit(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    animal_id = db.Column(
        db.Integer,
        db.ForeignKey('animal.id'),
        nullable=False
    )

    exit_type = db.Column(db.String(20))  # sale, slaughter, death

    quantity = db.Column(db.Integer, default=1)

    date = db.Column(db.Date)

    notes = db.Column(db.Text)

    animal = db.relationship('Animal')

    def __repr__(self):
        return f"<AnimalExit {self.exit_type}>"
    

############ BREEDING RECORD ##############

class BreedingEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    male_id = db.Column(
        db.Integer,
        db.ForeignKey('animal.id'),
        nullable=True
    )

    female_id = db.Column(
        db.Integer,
        db.ForeignKey('animal.id'),
        nullable=False
    )

    male_breed = db.Column(db.String(100))
    female_breed = db.Column(db.String(100))

    breeding_type = db.Column(db.String(20))  # Natural / AI

    breeding_date = db.Column(db.Date)
    expected_birth = db.Column(db.Date)

    status = db.Column(db.String(20), default="pregnant")

    notes = db.Column(db.Text)

    male = db.relationship("Animal", foreign_keys=[male_id])
    female = db.relationship("Animal", foreign_keys=[female_id])

    def __repr__(self):
        return f"<BreedingEvent {self.id}>"


########### BIRTH RECORDS ################

class Birth(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    breeding_event_id = db.Column(
        db.Integer,
        db.ForeignKey('breeding_event.id'),
        nullable=False
    )

    birth_date = db.Column(db.Date)

    offspring_breed = db.Column(db.String(100))

    male_offspring = db.Column(db.Integer, default=0)
    female_offspring = db.Column(db.Integer, default=0)

    notes = db.Column(db.Text)

    breeding_event = db.relationship("BreedingEvent")

    def __repr__(self):
        return f"<Birth {self.id}>"


##################################
#       FEEDING RECORDS          #
##################################

class FeedType(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    default_unit = db.Column(db.String(20))

    notes = db.Column(db.Text)

    def __repr__(self):
        return f"<FeedType {self.name}>"


class FeedRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    animal_id = db.Column(
        db.Integer,
        db.ForeignKey('animal.id'),
        nullable=False
    )

    feed_type_id = db.Column(
        db.Integer,
        db.ForeignKey('feed_type.id')
    )

    quantity = db.Column(db.Float)

    unit = db.Column(db.String(20))

    date = db.Column(db.Date)

    notes = db.Column(db.Text)

    animal = db.relationship("Animal")
    feed_type = db.relationship("FeedType")

    def __repr__(self):
        return f"<FeedRecord {self.id}>"
    

#################################
#       HEALTH MANAGEMENT       #
#################################

class HealthRecord(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    animal_id = db.Column(
        db.Integer,
        db.ForeignKey('animal.id'),
        nullable=False
    )

    condition = db.Column(db.String(150))

    treatment = db.Column(db.String(150))

    medication = db.Column(db.String(150))

    date = db.Column(db.Date)

    notes = db.Column(db.Text)

    animal = db.relationship("Animal")

    def __repr__(self):
        return f"<HealthRecord {self.id}>"


#############################
#           FINANCE         #
#############################

class FinanceTransaction(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String(20))

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('finance_category.id')
    )

    description = db.Column(db.String(200))
    amount = db.Column(db.Float)
    date = db.Column(db.Date)
    notes = db.Column(db.Text)

    category = db.relationship("FinanceCategory")


class FinanceCategory(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    type = db.Column(db.String(20))  # income / expense

    description = db.Column(db.String(200))

    def __repr__(self):
        return f"<FinanceCategory {self.name}>"


#############################
#           USERS           #
#############################

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    password_hash = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(50), default="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
    