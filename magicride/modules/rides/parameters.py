from magicride.modules.rides.models import Ride
from utilities import PatchJSONParameters


class PatchRideParameters(PatchJSONParameters):
    # pylint: disable=abstract-method,missing-docstring
    OPERATION_CHOICES = (
        PatchJSONParameters.OP_REPLACE,
    )

    PATH_CHOICES = tuple(
        '/%s' % field for field in (
            Ride.ride_name.key,
            Ride.min_age.key,
            Ride.min_height_in_cm.key,
        )
    )
