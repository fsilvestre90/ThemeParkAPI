from flask_marshmallow import base_fields
from marshmallow import validate

from utilities import Parameters


class LoginParameters(Parameters):
    """
    Helper parameters to login user.
    """
    email = base_fields.Email(
        description="the users email"
    )
    password = base_fields.String(
        description="the users password"
    )


class CreateUserParameters(Parameters):
    """
    Helper parameters to create user.
    """
    name = base_fields.String(
        description="the users name"
    )
    email = base_fields.Email(
        description="the users email"
    )
    password = base_fields.String(
        description="the users password"
    )


class CreateReviewParameters(Parameters):
    ride_id = base_fields.Integer(description="the ride our user is reviewing",
                                  validate=validate.Range(min=0, error="Invalid ride id"))
    user_id = base_fields.Integer(description="the user id who is reviewing",
                                  validate=validate.Range(min=0, error="Invalid user id"))
    description = base_fields.String(description="the users review")
    rating = base_fields.Integer(
        description="the users rating of a ride",
        validate=validate.Range(min=1, max=5, error="Invalid rating. Must be between 1-5")
    )
