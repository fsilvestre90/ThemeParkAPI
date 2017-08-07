from magicride.modules.users.models import User
from utilities import ModelSchema


class BaseUserSchema(ModelSchema):
    class Meta:
        model = User
        exclude = (
            User.id.key,
        )
