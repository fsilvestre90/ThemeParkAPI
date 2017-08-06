import logging

from magicride.extensions import db
from magicride.extensions.api import api_v1
from magicride.modules.geo import parameters
from magicride.modules.geo.models import Location
from magicride.modules.parks import schemas
from magicride.modules.parks.models import Park
from utilities import Resource
from utilities._http import HTTPStatus

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

parks_ns = api_v1.namespace(
    'parks', description="Park operations")  # pylint: disable=invalid-name


@parks_ns.route('/')
class AllParks(Resource):
    @parks_ns.response(schemas.BaseParkSchema(many=True))
    def get(self):
        """
        Get all parks.
        """
        return Park.get_all()


@parks_ns.route('/<int:park_id>')
@parks_ns.resolve_object_by_model(Park, 'park')
class ParkByID(Resource):
    @parks_ns.response(schemas.BaseParkSchema())
    def get(self, park):
        """
        Get park details by ID.
        """
        return park

    @parks_ns.response(code=HTTPStatus.CONFLICT)
    @parks_ns.response(code=HTTPStatus.NO_CONTENT)
    def delete(self, team):
        """
        Delete a park by ID.
        """
        with parks_ns.commit_or_abort(
                db.session,
                default_error_message="Failed to delete the park."
        ):
            parks_ns.session.delete(team)
        return None


@parks_ns.route('/nearest')
class ParksByLocation(Resource):
    @parks_ns.parameters(parameters.GeocodeParameters())
    @parks_ns.response(schemas.BaseParkSchema(many=True))
    def get(self, args):
        """
        Get parks by geocoordinates.
        """
        point = Location(latitude=args['latitude'], longitude=args['longitude'], radius=args['radius'])
        return Park.get_parks_by_point(point)
