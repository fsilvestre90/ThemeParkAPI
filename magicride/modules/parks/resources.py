import logging

from magicride.extensions import db
from magicride.extensions.api import api_v1
from magicride.extensions.api.parameters import GeocodeParameters
from magicride.modules.businesshours.models import BusinessHours
from magicride.modules.geo.models import Location
from magicride.modules.operators.models import Operator
from magicride.modules.parks.models import Park
from magicride.modules.parks.parameters import PatchParkParameters, CreateParkParameters
from magicride.modules.parks.schemas import ParkSchema
from magicride.modules.rides.models import Ride
from magicride.modules.rides.parameters import PatchRideParameters
from magicride.modules.rides.schemas import BaseRideSchema
from magicride.modules.sponsors.models import Sponsor
from utilities import Resource
from utilities._http import HTTPStatus

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

parks_ns = api_v1.namespace(
    'parks', description="Park operations")  # pylint: disable=invalid-name


@parks_ns.route('/')
class ParksIndex(Resource):
    @parks_ns.parameters(GeocodeParameters())
    @parks_ns.response(ParkSchema(many=True))
    def post(self, args):
        """
        Get all parks.
        """
        try:
            if args['filters']:
                filters = args['filters']
        except KeyError:
            filters = {}

        return Park.get_all(filters=filters)


@parks_ns.route('/new')
class CreatePark(Resource):
    @parks_ns.parameters(CreateParkParameters())
    @parks_ns.response(ParkSchema())
    def post(self, args):
        """
        Add a new park.
        """
        park = Park()
        park.name = args['name']
        park.address = args['address']
        park.admission_price = args['admission_price']
        park.operator_id = db.session.query(Operator.id).filter(Operator.name == args['operator']).first()

        business_hours = BusinessHours(opening_time=args['opening_time'], closing_time=args['closing_time'])
        location = Location(latitude=args['latitude'], longitude=args['longitude'])
        park.location = location.to_wkt_element()
        park.operating_hours = business_hours
        sponsors = Sponsor.find_if_none_create(args['sponsors'])
        park.sponsors = sponsors
        with parks_ns.commit_or_abort(
                db.session,
                default_error_message="Failed to create the park."
        ):
            db.session.add(park)

        return park


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
            db.session.delete(park)
        return None

    @parks_ns.response(ParkSchema())
    @parks_ns.response(code=HTTPStatus.CONFLICT)
    @parks_ns.response(code=HTTPStatus.NO_CONTENT)
    @parks_ns.parameters(PatchParkParameters())
    def put(self, args, park):
        """
        Update a park by ID.
        """
        with parks_ns.commit_or_abort(
                db.session,
                default_error_message="Failed to update the park."
        ):
            PatchParkParameters.perform_patch(args, obj=park)
            db.session.merge(park)
        return park


@parks_ns.route('/<int:park_id>/rides/<int:ride_id>')
@parks_ns.resolve_object_by_model(Park, 'park')
@parks_ns.resolve_object_by_model(Ride, 'ride')
class RideByParkID(Resource):
    # TODO: Finish endpoint
    @parks_ns.response(code=HTTPStatus.CONFLICT)
    @parks_ns.response(code=HTTPStatus.NO_CONTENT)
    def put(self, park, ride):
        """
        Delete a park ride by ID.
        """
        with parks_ns.commit_or_abort(
                db.session,
                default_error_message="Failed to delete the ride."
        ):
            db.session.delete(ride)
        return None

    @parks_ns.response(code=HTTPStatus.CONFLICT)
    @parks_ns.response(code=HTTPStatus.NO_CONTENT)
    def delete(self, park, ride):
        """
        Delete a ride by ID.
        """
        with parks_ns.commit_or_abort(
                db.session,
                default_error_message="Failed to delete the ride."
        ):
            db.session.delete(ride)
        return None

    @parks_ns.response(BaseRideSchema())
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
    @parks_ns.parameters(GeocodeParameters())
    @parks_ns.response(ParkSchema(many=True))
    def post(self, args):
        """
        Get parks by geolocation.
        """

        try:
            if args['filters']:
                filters = args['filters']
        except KeyError:
            filters = {}
        search_type = args['search']

        # Decide which query to use based on search param
        # refactor to use strategy pattern in future
        if 'point' in search_type:
            radius = int(args['radius'])
            point = Location(latitude=args['latitude'], longitude=args['longitude'])
            return Park.get_parks_by_point(point, radius=radius, filters=args['filters'])
        elif 'path' in search_type:
            points = [Location(latitude=coordinate[0], longitude=coordinate[1]) for coordinate in args['coordinates']]
            return Park.get_poi_along_path(points, args['radius'], filters=filters)
