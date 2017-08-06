from geoalchemy2 import Geometry

from magicride.extensions import db
from magicride.extensions.api.util_sqlalchemy import ResourceMixin
from magicride.modules.geo.models import Location
from magicride.modules.rides.models import Ride
from magicride.modules.sponsors.models import Sponsor


park_sponsors = db.Table('park_sponsors',
                         db.Column('park_id',
                                   db.Integer,
                                   db.ForeignKey('parks.id',
                                                 onupdate="CASCADE",
                                                 ondelete="CASCADE"),
                                   index=True,
                                   nullable=False),
                         db.Column('sponsor_id',
                                   db.Integer,
                                   db.ForeignKey('sponsors.id',
                                                 onupdate="CASCADE",
                                                 ondelete="CASCADE"),
                                   index=True,
                                   nullable=False))


class Park(ResourceMixin, db.Model):
    __tablename__ = 'parks'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    location = db.Column('location', Geometry(geometry_type='POINT'))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    admission_price = db.Column(db.Float, nullable=False)

    # Relationships
    operator_id = db.Column(db.Integer, db.ForeignKey('operators.id',
                                                      onupdate="CASCADE",
                                                      ondelete="CASCADE"),
                            index=True, nullable=False)

    business_hours = db.Column(db.Integer, db.ForeignKey('business_hours.id',
                                                         onupdate="CASCADE",
                                                         ondelete="CASCADE"),
                               index=True, nullable=False)

    sponsors = db.relationship(Sponsor,
                               secondary=park_sponsors,
                               backref='park_sponsors',
                               lazy='dynamic',
                               passive_deletes=True)

    rides = db.relationship(Ride,
                            backref='park',
                            lazy='dynamic',
                            passive_deletes=True)

    def __init__(self, **kwargs):
        location = Location(latitude=kwargs.get('lat', 0),
                            longitude=kwargs.get('lng', 0))
        self.location = location.to_wkt_element()
        super(Park, self).__init__()

    @classmethod
    def get_parks_by_point(cls, point):
        """
        Get parks within given coordinates and radius.
        :param: point: a Location instance
        :return: list of parks found
        """
        print(point.to_wkt_element())
        return db.session \
            .query(Park) \
            .filter(db.func.ST_DWithin(Park.location, point.to_wkt_element(),
                                       point.radius)) \
            .all()

    @classmethod
    def get_all(cls):
        """
        Retrieve all active Parks.

        :return: Park instance
        """
        return Park.query.filter(Park.is_active == True).all()
