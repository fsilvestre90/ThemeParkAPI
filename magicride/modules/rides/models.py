from sqlalchemy import func

from magicride.extensions import db
from magicride.extensions.api.util_sqlalchemy import ResourceMixin
from magicride.modules.reviews.models import Review


class RideType(ResourceMixin, db.Model):
    __tablename__ = 'ride_types'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ride_type = db.Column(db.String, nullable=False)


class Ride(ResourceMixin, db.Model):
    __tablename__ = 'rides'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ride_name = db.Column(db.String, nullable=False)
    min_height_in_cm = db.Column(db.Float, nullable=False)
    min_age = db.Column(db.Integer, nullable=False)
    average_rating = db.Column(db.Float, default=0)

    # Relationships
    ride_type_id = db.Column(db.Integer, db.ForeignKey('ride_types.id',
                                                       onupdate="CASCADE",
                                                       ondelete="CASCADE"),
                             index=True, nullable=False)

    park_id = db.Column(db.Integer, db.ForeignKey('parks.id',
                                                  onupdate="CASCADE",
                                                  ondelete="CASCADE"),
                        index=True, nullable=False)

    ride_type = db.relationship(RideType, foreign_keys=[ride_type_id])

    reviews = db.relationship(Review, backref='rides',
                              lazy='dynamic',
                              passive_deletes=True)

    def update_average_rating(self):
        new_rating = db.session.query(
            func.avg(Review.rating).label("average_rating")
        ).filter(Review.ride_id == self.id).first()
        self.average_rating = round(new_rating[0], 1)
