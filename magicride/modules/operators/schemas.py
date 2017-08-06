from magicride.modules.operators.models import Operator
from utilities import ModelSchema


class BaseOperatorSchema(ModelSchema):

    class Meta:
        model = Operator
        exclude = (
            Operator.id.key,
            Operator.park.key,
        )
