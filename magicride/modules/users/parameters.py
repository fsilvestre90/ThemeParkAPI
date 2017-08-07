from utilities import Parameters
from flask_marshmallow import base_fields


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
    email = base_fields.Email(
        description="the users email"
    )
    password = base_fields.String(
        description="the users password"
    )