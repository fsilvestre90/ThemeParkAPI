from magicride.extensions import db
from magicride.extensions.api.util_sqlalchemy import ResourceMixin
from magicride.modules.reviews.models import Review


class Ride(ResourceMixin, db.Model):
    __tablename__ = 'rides'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ride_name = db.Column(db.String, nullable=False)
    min_height_in_cm = db.Column(db.Float, nullable=False)
    min_age = db.Column(db.Integer, nullable=False)

    # Relationships
    ride_type_id = db.Column(db.Integer, db.ForeignKey('ride_types.id',
                                                       onupdate="CASCADE",
                                                       ondelete="CASCADE"),
                             index=True, nullable=False)

    park_id = db.Column(db.Integer, db.ForeignKey('parks.id',
                                                  onupdate="CASCADE",
                                                  ondelete="CASCADE"),
                        index=True, nullable=False)

    reviews = db.relationship(Review, backref='rides',
                              lazy='dynamic',
                              passive_deletes=True)


class RideType(ResourceMixin, db.Model):
    __tablename__ = 'ride_types'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ride_type = db.Column(db.String, nullable=False)
