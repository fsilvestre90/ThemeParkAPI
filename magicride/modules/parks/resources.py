import logging

import flask
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest

from magicride.extensions.api import api_v1
from magicride.modules.geo import parameters
from magicride.modules.geo.models import Location
from magicride.modules.parks import schemas
from magicride.modules.parks.models import Park

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

parks_ns = api_v1.namespace(
    'parks', description="Park operations")  # pylint: disable=invalid-name


@parks_ns.route('/')
class AllParks(Resource):
    @parks_ns.response(schemas.BaseParkSchema(many=True))
    def get(self):
        return Park.get_all()


@parks_ns.route('/nearest')
class ParksByLocation(Resource):

    @parks_ns.parameters(parameters.GeocodeParameters())
    @parks_ns.response(schemas.BaseParkSchema(many=True))
    def get(self, args):
        # geocode = [item.encode('utf8') for item in flask.request.args.get("geocode").split(",")]
        point = Location(latitude=args['latitude'], longitude=args['longitude'], radius=args['radius'])
        #
        # if len(geocode) < 2 or len(geocode) > 3 or not point.is_valid_latitude() or not point.is_valid_longitude():
        #     if len(geocode) < 2:
        #         raise BadRequest('Incomplete coordinate parameters.')
        #     if len(geocode) > 3:
        #         raise BadRequest('Too many parameters entered. Max is 3')
        #     if not point.is_valid_latitude():
        #         raise BadRequest('Invalid latitude parameters. Must be between -90 and 90.')
        #     if not point.is_valid_longitude():
        #         raise BadRequest('Invalid longitude parameters. Must be between -180 and 180.')

        return Park.get_parks_by_point(point)
