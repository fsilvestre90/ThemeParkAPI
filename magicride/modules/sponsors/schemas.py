from magicride.modules.sponsors.models import Sponsor
from utilities import ModelSchema


class BaseSponsorSchema(ModelSchema):

    class Meta:
        model = Sponsor
        fields = (
            Sponsor.name.key,
        )
