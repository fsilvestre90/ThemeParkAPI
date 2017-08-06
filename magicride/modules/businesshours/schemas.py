from magicride.modules.businesshours.models import BusinessHours
from utilities import ModelSchema


class BaseParkSchema(ModelSchema):

    class Meta:
        model = BusinessHours
