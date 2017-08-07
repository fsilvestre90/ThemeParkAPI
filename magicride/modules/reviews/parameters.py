from flask_marshmallow import base_fields
from marshmallow import validate

from utilities import Parameters


class CreateReviewParameters(Parameters):
    description = base_fields.String(description="the users review")
    rating = base_fields.Integer(
        description="the users rating of a ride",
        validate=validate.Range(min=1, max=5, error="Invalid rating. Must be between 1-5")
    )
