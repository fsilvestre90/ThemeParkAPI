import math

from flask_restplus import abort
from geoalchemy2 import Geometry, WKTElement
from geoalchemy2.shape import to_shape

from magicride.extensions import db
from magicride.extensions.api.util_sqlalchemy import ResourceMixin
from magicride.modules.rides.models import Ride

park_sponsors = db.Table('park_sponsors',
                         db.Column('park_id',
                                   db.Integer,
                                   db.ForeignKey('parks.id', onupdate="CASCADE", ondelete="CASCADE")),
                         db.Column('sponsor_id',
                                   db.Integer,
                                   db.ForeignKey('sponsors.id', onupdate="CASCADE", ondelete="CASCADE")))


class BusinessHours(db.Model):
    __tablename__ = 'business_hours'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    days_opened = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    close_time = db.Column(db.Time, nullable=False)
    park_id = db.Column(db.Integer, db.ForeignKey(
        'parks.id', onupdate="CASCADE", ondelete="CASCADE"))


class Sponsor(db.Model):
    __tablename__ = 'sponsors'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)


class Park(ResourceMixin, db.Model):
    __tablename__ = 'parks'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    location = db.Column('location', Geometry(geometry_type='POINT'))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    admission_price = db.Column(db.Float, nullable=False)
    operator_id = db.Column(db.Integer, db.ForeignKey('operators.id',
                                                      onupdate="CASCADE",
                                                      ondelete="CASCADE"))

    business_hours = db.relationship(BusinessHours,
                                     backref="parks",
                                     lazy='dynamic')

    sponsors = db.relationship(Sponsor,
                               secondary=park_sponsors,
                               backref='park_sponsors',
                               lazy='dynamic')

    rides = db.relationship(Ride,
                            backref='parks',
                            lazy='dynamic')

    # reviews = db.relationship('reviews', backref='reviews',
    #                           lazy='dynamic')

    def __init__(self, **kwargs):
        location = Location(latitude=kwargs.get('lat', 0),
                            longitude=kwargs.get('lng', 0))
        self.location = location.to_wkt_element()
        super(Park, self).__init__()

    @classmethod
    def get_rides_by_point(cls, point, radius):
        return db.session \
            .query(Park) \
            .filter(db.func.ST_DWithin(Park.location, point.to_wkt_element(), radius)) \
            .all()


class Operator(db.Model):
    __tablename__ = 'operators'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    park = db.relationship(Park,
                           backref="operators",
                           lazy='dynamic')


class Location(object):
    def __init__(self, latitude=None, longitude=None):
        self.latitude = latitude
        self.longitude = longitude

    def to_wkt(self):
        return 'POINT({0} {1})'.format(self.longitude, self.latitude)

    def to_wkt_element(self, srid=4326):
        if not srid:
            srid = -1
        return WKTElement(self.to_wkt(), srid=srid)

    def make_point(self, srid=4326):
        point = db.func.ST_MakePoint(self.longitude, self.latitude)
        if srid:
            point = db.func.ST_SetSRID(point, srid)
        return point

    @staticmethod
    def from_wkb(wkb):
        coords = to_shape(wkb)
        return Location(latitude=coords.y, longitude=coords.x)

    @staticmethod
    def parse_location(args):
        try:
            latitude = float(args['lat'])
            longitude = float(args['lon'])
            return Location(latitude=latitude, longitude=longitude)

        except (KeyError, ValueError):
            abort(400)

    def __str__(self):
        return self.to_wkt()


class BoundingBox(object):
    """
    A 2D bounding box
    """

    def __init__(self, latitude_in_degrees, longitude_in_degrees, half_side_in_miles):
        assert half_side_in_miles > 0
        assert -90.0 <= latitude_in_degrees <= 90.0
        assert -180.0 <= longitude_in_degrees <= 180.0

        half_side_in_km = half_side_in_miles * 1.609344
        lat = math.radians(latitude_in_degrees)
        lon = math.radians(longitude_in_degrees)

        radius = 6371
        # Radius of the parallel at given latitude
        parallel_radius = radius * math.cos(lat)

        lat_min = lat - half_side_in_km / radius
        lat_max = lat + half_side_in_km / radius
        lon_min = lon - half_side_in_km / parallel_radius
        lon_max = lon + half_side_in_km / parallel_radius
        rad2deg = math.degrees

        self.northeast = Location(rad2deg(lat_max), rad2deg(lon_max))
        self.southwest = Location(rad2deg(lat_min), rad2deg(lon_min))

    def make_st_box(self, srid=4326):
        box = db.func.ST_MakeBox2D(self.southwest.make_point(),
                                   self.northeast.make_point())
        if srid:
            box = db.func.ST_SetSRID(box, srid)

        return box
