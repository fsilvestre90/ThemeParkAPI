from flask_marshmallow import base_fields

from utilities import PostFormParameters


class LoginParameters(PostFormParameters):
    """
    Helper parameters to login user.
    """
    email = base_fields.Email(
        description="the users email"
    )
    password = base_fields.String(
        description="the users password"
    )


class CreateUserParameters(PostFormParameters):
    """
    Helper parameters to create user.
    """
    email = base_fields.Email(
        description="the users email"
    )
    password = base_fields.String(
        description="the users password"
    )