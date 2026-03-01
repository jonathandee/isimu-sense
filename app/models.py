from . import db

class InventoryCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<InventoryCategory {self.name}>"