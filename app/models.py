from . import db

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

