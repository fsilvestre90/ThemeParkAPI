from magicride.modules.reviews.schemas import ReviewSchema
from magicride.modules.users.models import User
from flask_marshmallow import base_fields
from utilities import ModelSchema


class BaseUserSchema(ModelSchema):
    reviews = base_fields.Nested(ReviewSchema, many=True)

    class Meta:
        model = User


class LoginUserSchema(BaseUserSchema):
    class Meta:
        model = User
        fields = (
            User.id.key,
            User.email.key,
            User.name.key
        )


class ReviewsUserSchema(BaseUserSchema):

    class Meta:
        model = User
        fields = (
            User.id.key,
            User.email.key,
            User.name.key,
        )
