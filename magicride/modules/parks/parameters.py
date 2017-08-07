from marshmallow import validate

from magicride.modules.parks.models import Park
from utilities import PatchJSONParameters, Parameters
from flask_marshmallow import base_fields


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


class CreateParkParameters(Parameters):
    """
    Helper Parameters class to reuse geocoding.
    """
    latitude = base_fields.Float(
        description="the latitude to search in",
        validate=validate.Range(min=-90.0, max=90.0, error="Invalid latitude parameters. Must be between -90 and 90.")
    )
    longitude = base_fields.Float(
        description="the latitude to search in",
        validate=validate.Range(min=-180.0, max=180.0,
                                error="Invalid longitude parameters. Must be between -180 and 180.")
    )
    radius = base_fields.Float(
        description="the radius to search in",
        missing=5,
        validate=validate.Range(min=0)
    )
