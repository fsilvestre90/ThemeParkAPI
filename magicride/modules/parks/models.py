from geoalchemy2 import Geometry
from sqlalchemy import func, desc, and_

from magicride.extensions import db
from magicride.extensions.api.util_sqlalchemy import ResourceMixin
from magicride.modules.businesshours.models import BusinessHours
from magicride.modules.geo.models import Location, RoutePaths
from magicride.modules.operators.models import Operator
from magicride.modules.rides.models import Ride, RideType
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
    location = db.Column('location', Geometry(geometry_type='POINT', srid=4326))
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

    operator = db.relationship(Operator, foreign_keys=[operator_id])

    operating_hours = db.relationship(BusinessHours, foreign_keys=[business_hours])

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
    def get_parks_by_point(cls, point, radius=5, filters=None):
        if filters is None:
            filters = {}
        """
        Get parks within given coordinates and radius.
        :param: point: a Location instance
        :param filters: filters for searching
        :return: list of parks
        """
        q = db.session \
            .query(Park) \
            .filter(db.func.ST_DWithin(Park.location,
                                       point.to_wkt_element(),
                                       radius)) \

        final = _combine_filters(q, filters)

        return final.all()

    @classmethod
    def get_poi_along_path(cls, lines, radius=5, filters=None):
        if filters is None:
            filters = {}

        """
        SELECT park.*
        FROM park
        WHERE ST_DWithin(line.geom, park.geom, radius)
        ORDER BY ST_Line_Locate_Point(line.geom, park.geom),
                 ST_Distance(line.geom, park.geom);

        :param lines: an array of locations
        :param radius: the search radius
        :param filters: filters for searching
        :return: list of all POI's found
        """
        linestring = RoutePaths(paths=lines)
        q = db.session.query(Park).join(Ride).filter(func.ST_DWithin(linestring.locations,
                                                                     Park.location,
                                                                     radius)) \
            .order_by(
            desc(func.ST_Line_Locate_Point(linestring.locations, Park.location)),
            desc(func.ST_Distance(linestring.locations, Park.location)))

        final = _combine_filters(q, filters)

        return final.all()

    @classmethod
    def get_all(cls, filters):
        if filters is None:
            filters = {}

        """
        Retrieve all active Parks.
        :param filters: filters for searching
        :return: Park instance
        """
        q = Park.query.filter(Park.is_active == True)

        final = _combine_filters(q, filters)

        return final.all()


def _combine_filters(query, filters):
    for attr, value in filters.items():
        if 'operator' in attr:
            query = query.join(Operator).filter(and_(Operator.name == value))
        elif 'admission_price' in attr:
            query = query.filter(and_(Park.admission_price <= value))
        elif 'ride_type' in attr:
            filter_ride_list = [item.encode('UTF8') for item in value]
            for i in filter_ride_list:
                query = query.filter(and_(RideType.ride_type.in_(filter_ride_list)))
        elif 'min_height_in_cm' in attr:
            query = query.filter(and_(Ride.min_height_in_cm <= value))
    return query
