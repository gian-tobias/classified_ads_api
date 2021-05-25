import enum
from app import db


class AdCategory(enum.Enum):
    CARS = "cars"
    REAL_ESTATE = "real_estate"
    CLOTHING = "clothing"
    ELECTRONICS = "electronics"
    FOOD = "food"
    TRAVEL = "travel"


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    advertisement = db.relationship("Advertisement",
                                    backref=db.backref("user", lazy=True))


class Advertisement(db.Model):
    __tablename__ = 'advertisement'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True, nullable=False)
    category = db.Column(db.Enum(AdCategory), nullable=False)
    description = db.Column(db.String(), nullable=False)
    owner_username = db.Column(db.String(), db.ForeignKey("user.username"))

    def update(self, **kwargs):
        updated_pairs = {}
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                updated_pairs[key] = value
        return updated_pairs
