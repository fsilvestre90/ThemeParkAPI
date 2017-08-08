from magicride.extensions import db
from magicride.extensions.api.util_sqlalchemy import ResourceMixin


class Sponsor(ResourceMixin, db.Model):
    __tablename__ = 'sponsors'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)

    @classmethod
    def find_if_none_create(cls, sponsors):
        found = db.session.query(Sponsor).filter(Sponsor.name.in_(sponsors)).all()
        if not found:
            db.session.begin()
            for name in sponsors:
                new = Sponsor()
                new.name = name
                db.session.add(new)
            db.session.commit()
            return db.session.query(Sponsor).filter(Sponsor.name.in_(sponsors)).all()
        return found
