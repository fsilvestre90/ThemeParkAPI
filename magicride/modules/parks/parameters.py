from magicride.modules.parks.models import Park
from utilities import PatchJSONParameters


class PatchParkParameters(PatchJSONParameters):
    # pylint: disable=abstract-method,missing-docstring
    OPERATION_CHOICES = (
        PatchJSONParameters.OP_REPLACE,
    )

    PATH_CHOICES = tuple(
        '/{0}'.format(field) for field in (
            Park.name.key,
            Park.address.key,
            Park.location.key,
            Park.is_active.key,
            Park.admission_price.key,
        )
    )
