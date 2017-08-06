from magicride.extensions import db


class Sponsor(db.Model):
    __tablename__ = 'sponsors'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)