from magicride.extensions import db


class Operator(db.Model):
    __tablename__ = 'operators'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, index=True, nullable=False)
