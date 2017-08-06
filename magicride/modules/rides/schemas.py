from magicride.modules.rides.models import Ride
from utilities import ModelSchema


class BaseRideSchema(ModelSchema):
    class Meta:
        model = Ride
        exclude = (
            Ride.park.key,
        )


class RideNoReviews(BaseRideSchema):
    class Meta:
        exclude = (
            Ride.reviews.key,
        )
