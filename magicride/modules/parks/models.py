from geoalchemy2 import Geometry
from sqlalchemy import func

from magicride.extensions import db
from magicride.extensions.api.util_sqlalchemy import ResourceMixin
from magicride.modules.geo.models import Location, RoutePaths
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
    def get_parks_by_point(cls, point, radius=5):
        """
        Get parks within given coordinates and radius.
        :param: point: a Location instance
        :return: list of parks
        """
        return db.session \
            .query(Park) \
            .filter(db.func.ST_DWithin(Park.location,
                                       point.to_wkt(),
                                       radius)) \
            .all()

    @classmethod
    def get_poi_along_path(cls, lines, radius=5):
        """
        SELECT 
            ST_AsText(
                ST_line_interpolate_point(
                    line_geom,
                    ST_line_locate_point(line_geom, point_geom)
                )
            )
        FROM
        (
            SELECT
                linestring AS line_geom,
                park.location AS point_geom
            FROM
                park
            WHERE
                ST_DWithin(linestring, park.location, 5)
        ) AS sub_query;
        
        :param lines: an array of locations
        :param radius: the search radius     
        :return: list of all POI's found
        """
        linestring = RoutePaths(paths=lines)

        sub_query = db.session.query(linestring.locations.label("line_geom"),
                                     Park.location.label("point_geom")) \
            .filter(func.ST_DWithin(linestring.locations,
                                    Park.location,
                                    radius)) \
            .subquery()

        return db.session.query(
            func.ST_AsText(
                func.ST_Line_Interpolate_Point(
                    sub_query.c.line_geom, func.ST_Line_Locate_Point(sub_query.c.line_geom, sub_query.c.point_geom)))) \
            .all()

    @classmethod
    def get_all(cls):
        """
        Retrieve all active Parks.

        :return: Park instance
        """
        return Park.query.filter(Park.is_active == True).all()
