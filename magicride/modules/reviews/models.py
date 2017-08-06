from magicride.extensions import db
from magicride.extensions.api.util_sqlalchemy import ResourceMixin


class Review(ResourceMixin, db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Relationships
    ride_id = db.Column(db.Integer, db.ForeignKey('rides.id',
                                                  onupdate="CASCADE",
                                                  ondelete="CASCADE"),
                        index=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id',
                                                  onupdate="CASCADE",
                                                  ondelete="CASCADE"),
                        index=True, nullable=False)
