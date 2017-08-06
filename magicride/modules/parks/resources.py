import logging

import flask
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest

from magicride.extensions.api import api_v1
from magicride.modules.parks import schemas
from magicride.modules.parks.models import Park, Location

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

parks_ns = api_v1.namespace(
    'parks', description="Bathroom operations")  # pylint: disable=invalid-name


@parks_ns.route('/')
class ParksIndex(Resource):

    def get(self):
        lat = float(flask.request.args.get("lat"))
        lng = float(flask.request.args.get("lng"))

        point = Location(latitude=lat, longitude=lng)
        if not point:
            raise BadRequest('Invalid coordinate parameters.')
        return schemas.BaseParkSchema() \
                      .dump(Park.get_bathrooms(point), many=True)
