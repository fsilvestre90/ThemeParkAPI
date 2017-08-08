from magicride.extensions import db


class BusinessHours(db.Model):
    __tablename__ = 'business_hours'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    opening_time = db.Column(db.Time, nullable=False)
    closing_time = db.Column(db.Time, nullable=False)
