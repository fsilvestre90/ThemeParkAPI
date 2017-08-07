from magicride.modules.rides.models import Ride, RideType
from flask_marshmallow import base_fields

from utilities import ModelSchema


class BaseRideTypeSchema(ModelSchema):
    class Meta:
        model = RideType
        fields = (
            RideType.ride_type.key,
        )


class BaseRideSchema(ModelSchema):
    ride_type = base_fields.Nested(BaseRideTypeSchema)

    class Meta:
        model = Ride
        exclude = (
            Ride.park.key,
            Ride.reviews.key
        )
