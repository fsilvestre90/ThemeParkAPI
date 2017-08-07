import logging

from magicride.extensions import db
from magicride.extensions.api import api_v1
from magicride.modules.geo import parameters
from magicride.modules.geo.models import Location
from magicride.modules.parks.models import Park
from magicride.modules.parks.schemas import ParkSchema
from magicride.modules.rides.models import Ride
from magicride.modules.rides.parameters import PatchRideParameters
from magicride.modules.rides.schemas import BaseRideSchema
from utilities import Resource
from utilities._http import HTTPStatus

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

parks_ns = api_v1.namespace(
    'parks', description="Park operations")  # pylint: disable=invalid-name


@parks_ns.route('/')
class AllParks(Resource):
    @parks_ns.response(ParkSchema(many=True))
    def get(self):
        """
        Get all parks.
        """
        return Park.get_all()


@parks_ns.route('/<int:park_id>')
@parks_ns.resolve_object_by_model(Park, 'park')
class ParkByID(Resource):
    @parks_ns.response(ParkSchema())
    def get(self, park):
        """
        Get park details by ID.
        """
        return park

    @parks_ns.response(code=HTTPStatus.CONFLICT)
    @parks_ns.response(code=HTTPStatus.NO_CONTENT)
    def delete(self, park):
        """
        Delete a park by ID.
        """
        with parks_ns.commit_or_abort(
                db.session,
                default_error_message="Failed to delete the park."
        ):
            parks_ns.session.delete(park)
        return None

    @parks_ns.response(code=HTTPStatus.CONFLICT)
    @parks_ns.response(code=HTTPStatus.NO_CONTENT)
    def put(self, park):
        """
        Update a park by ID.
        """
        with parks_ns.commit_or_abort(
                db.session,
                default_error_message="Failed to update the park."
        ):
            parks_ns.session.merge(park)
        return None


@parks_ns.route('/<int:park_id>/rides/<int:ride_id>')
@parks_ns.resolve_object_by_model(Park, 'park')
@parks_ns.resolve_object_by_model(Ride, 'ride')
class RideByParkID(Resource):
    @parks_ns.response(BaseRideSchema(), many=True)
    def get(self, park, ride):
        """
        Get a park ride.
        """
        return ride

    @parks_ns.response(code=HTTPStatus.CONFLICT)
    @parks_ns.response(code=HTTPStatus.NO_CONTENT)
    def delete(self, park, ride):
        """
        Delete a park ride by ID.
        """
        with parks_ns.commit_or_abort(
                db.session,
                default_error_message="Failed to delete the ride."
        ):
            db.session.delete(ride)
        return None

    @parks_ns.response(BaseRideSchema(), many=True)
    @parks_ns.response(code=HTTPStatus.CONFLICT)
    @parks_ns.response(code=HTTPStatus.NO_CONTENT)
    @parks_ns.parameters(PatchRideParameters())
    def put(self, args, park, ride):
        """
        Update a ride by ID.
        """
        with parks_ns.commit_or_abort(
                db.session,
                default_error_message="Failed to update the ride."
        ):
            PatchRideParameters.perform_patch(args, obj=ride)
            db.session.merge(ride)
        return ride


@parks_ns.route('/nearest')
class ParksByLocation(Resource):
    @parks_ns.parameters(parameters.GeocodeParameters())
    @parks_ns.response(ParkSchema(many=True))
    def get(self, args):
        """
        Get parks by geocoordinates.
        """
        point = Location(latitude=args['latitude'], longitude=args['longitude'], radius=args['radius'])
        return Park.get_parks_by_point(point)
