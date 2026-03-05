from . import db

class InventoryCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<InventoryCategory {self.name}>"

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

    crop_type = db.relationship('CropType')
    field = db.relationship('Field')

    def __repr__(self):
        return f"<Planting {self.id}>"