from magicride.extensions import db
from magicride.extensions.api.util_sqlalchemy import ResourceMixin


class Bookmark(ResourceMixin, db.Model):
    __tablename__ = 'bookmarks'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ride_id = db.Column(db.Integer, db.ForeignKey('rides.id',
                                                  onupdate="CASCADE",
                                                  ondelete="CASCADE"),
                        index=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id',
                                                  onupdate="CASCADE",
                                                  ondelete="CASCADE"),
                        index=True, nullable=False)
