from flask import logging

from magicride.extensions import db
from magicride.extensions.api import api_v1
from magicride.modules.reviews.models import Review
from magicride.modules.reviews.schemas import BaseReviewSchema
from magicride.modules.rides.models import Ride
from magicride.modules.users.parameters import CreateReviewParameters
from utilities import Resource

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

reviews_ns = api_v1.namespace(
    'reviews', description="Review operations")  # pylint: disable=invalid-name


@reviews_ns.route('/')
class ReviewsIndex(Resource):
    @reviews_ns.parameters(CreateReviewParameters())
    @reviews_ns.response(BaseReviewSchema())
    def post(self, args):
        """
        Create a new review.
        """
        with reviews_ns.commit_or_abort(
                db.session,
                default_error_message="Failed to create a new review."
        ):
            # submit new review
            new_review = Review(user_id=args['user_id'],
                                ride_id=args['ride_id'],
                                description=args['description'],
                                rating=args['rating'])
            db.session.add(new_review)

            # update ride average rating
            ride = db.session.query(Ride).filter(Ride.id == new_review.ride_id).first()
            ride.update_average_rating()
        return new_review
