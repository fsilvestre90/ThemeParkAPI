import logging

import flask
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest

from magicride.extensions.api import api_v1
from magicride.modules.parks import schemas
from magicride.modules.parks.models import Park
from magicride.modules.geo.models import Location

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

parks_ns = api_v1.namespace(
    'parks', description="Park operations")  # pylint: disable=invalid-name


@parks_ns.route('/')
class AllParks(Resource):

    def get(self):
        return schemas.BaseParkSchema() \
                      .dump(Park.get_all(), many=True)


@parks_ns.route('/location')
class RidesByLocation(Resource):

    def get(self):
        lat = float(flask.request.args.get("lat"))
        lng = float(flask.request.args.get("lng"))
        radius = flask.request.args.get("radius")

        point = Location(latitude=lat, longitude=lng)
        if not point:
            raise BadRequest('Invalid coordinate parameters.')
        return schemas.BaseParkSchema() \
                      .dump(Park.get_rides_by_point(point, radius), many=True)
