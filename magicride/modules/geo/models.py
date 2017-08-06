import math

from geoalchemy2 import WKTElement
from geoalchemy2.shape import to_shape

from magicride.extensions import db


class Location(object):
    """
    A location wrapper to help with PostGIS stuff

    :param latitude: a latitude
    :type latitude: double

    :param longitude: a longitude
    :type longitude: double

    :return: Location instance
    """

    def __init__(self, latitude=None, longitude=None):
        self.latitude = latitude
        self.longitude = longitude

    def to_wkt(self):
        """
        Converts class objects to a WKTElement string representation

        :return: str
        """
        return 'POINT({0} {1})'.format(self.longitude, self.latitude)

    def to_wkt_element(self, srid=4326):
        """
        Converts class objects to a WKTElement

        :param srid: a spatial reference system identifier
        :type srid: int
        :return: WKTElement
        """
        if not srid:
            srid = -1
        return WKTElement(self.to_wkt(), srid=srid)

    def make_point(self, srid=4326):
        """
        Creates a point

        :param srid: a spatial reference system identifier
        :type srid: int
        :return: PostGIS point
        """
        point = db.func.ST_MakePoint(self.longitude, self.latitude)
        if srid:
            point = db.func.ST_SetSRID(point, srid)
        return point

    @staticmethod
    def from_wkb(wkb):
        """
        Converts Well-Known Binary geometry representation (WKB)
        to location instance

        :param wkb: Well-Known Binary geometry representation (WKB)
        :type wkb: wkb instance
        :return: Location instance
        """
        coords = to_shape(wkb)
        return Location(latitude=coords.y, longitude=coords.x)

    def __str__(self):
        return self.to_wkt()


class BoundingBox(object):
    """
    A 2D bounding box

    :param latitude: Latitude to search in
    :type latitude: double

    :param longitude: Latitude to search in
    :type longitude: double

    :param miles: miles to search around
    :type miles: int

    :return: BoundingBox instance
    """

    def __init__(self, latitude, longitude, miles):
        assert miles > 0
        assert -90.0 <= latitude <= 90.0
        assert -180.0 <= longitude <= 180.0

        mi_to_km = miles * 1.609344
        lat = math.radians(latitude)
        lon = math.radians(longitude)

        radius = 6371
        # Radius of the parallel at given latitude
        parallel_radius = radius * math.cos(lat)

        lat_min = lat - mi_to_km / radius
        lat_max = lat + mi_to_km / radius
        lon_min = lon - mi_to_km / parallel_radius
        lon_max = lon + mi_to_km / parallel_radius
        rad2deg = math.degrees

        self.northeast = Location(rad2deg(lat_max), rad2deg(lon_max))
        self.southwest = Location(rad2deg(lat_min), rad2deg(lon_min))

    def make_st_box(self, srid=4326):
        """
        :param srid: a spatial reference system identifier
        :type srid: int
        :return: ST_MakeBox2D instance
        """
        box = db.func.ST_MakeBox2D(self.southwest.make_point(),
                                   self.northeast.make_point())
        if srid:
            box = db.func.ST_SetSRID(box, srid)

        return box
