from magicride.modules.operators.models import Operator
from utilities import ModelSchema


class BaseOperatorSchema(ModelSchema):

    class Meta:
        model = Operator
        fields = (
            Operator.name.key,
        )
