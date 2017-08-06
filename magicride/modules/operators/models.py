from magicride.extensions import db
from magicride.modules.parks.models import Park


class Operator(db.Model):
    __tablename__ = 'operators'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    park = db.relationship(Park,
                           uselist=False,
                           backref="operator")