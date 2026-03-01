from . import db

class InventoryCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<InventoryCategory {self.name}>"

class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    variety = db.Column(db.String(100))
    planting_date = db.Column(db.String(50))
    expected_harvest = db.Column(db.String(50))

    def __repr__(self):
        return f"<Crop {self.name}>"