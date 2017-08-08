from flask import logging

from magicride.extensions import db
from magicride.extensions.api import api_v1
from magicride.modules.reviews.models import Review
from magicride.modules.reviews.schemas import ReviewSchema
from magicride.modules.rides.models import Ride
from magicride.modules.users.models import User
from magicride.modules.users.parameters import CreateReviewParameters
from utilities import Resource
from utilities._http import HTTPStatus

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

reviews_ns = api_v1.namespace(
    'reviews', description="Review operations")  # pylint: disable=invalid-name


@reviews_ns.route('/<int:user_id>/ride/<int:ride_id>')
@reviews_ns.resolve_object_by_model(User, 'user')
@reviews_ns.resolve_object_by_model(Ride, 'ride')
class ReviewsIndex(Resource):
    @reviews_ns.parameters(CreateReviewParameters())
    @reviews_ns.response(ReviewSchema())
    @reviews_ns.response(code=HTTPStatus.CONFLICT)
    @reviews_ns.response(code=HTTPStatus.NO_CONTENT)
    def post(self, args, user, ride):
        """
        Create a new review.
        """

        with reviews_ns.commit_or_abort(
                db.session,
                default_error_message="Failed to create a new review."
        ):
            # submit new review
            new_review = Review()
            new_review.user_id = user.id,
            new_review.ride_id = ride.id,
            new_review.description = args['description'],
            new_review.rating = args['rating']

            db.session.add(new_review)

            # update ride average rating
            ride = db.session.query(Ride).filter(Ride.id == new_review.ride_id).first()
            ride.update_average_rating()
            return new_review
