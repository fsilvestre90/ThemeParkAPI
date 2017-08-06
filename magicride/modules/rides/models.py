from magicride.extensions import db
from magicride.extensions.api.util_sqlalchemy import ResourceMixin
from magicride.modules.reviews.models import Review


class Ride(ResourceMixin, db.Model):
    __tablename__ = 'rides'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ride_name = db.Column(db.String, nullable=False)
    min_height_in_cm = db.Column(db.Float, nullable=False)
    min_age = db.Column(db.Integer, nullable=False)
    ride_type_id = db.Column(db.Integer, db.ForeignKey('ride_types.id'))
    park_id = db.Column(db.Integer, db.ForeignKey('parks.id',
                                                  onupdate="CASCADE",
                                                  ondelete="CASCADE"))

    reviews = db.relationship(Review, backref='rides',
                              lazy='dynamic')


class RideType(ResourceMixin, db.Model):
    __tablename__ = 'ride_types'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ride_type = db.Column(db.String, nullable=False)
