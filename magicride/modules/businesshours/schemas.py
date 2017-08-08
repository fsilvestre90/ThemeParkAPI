from magicride.modules.businesshours.models import BusinessHours
from utilities import ModelSchema


class BaseBusinessHoursSchema(ModelSchema):

    class Meta:
        model = BusinessHours
        exclude = (
            BusinessHours.id.key,
        )