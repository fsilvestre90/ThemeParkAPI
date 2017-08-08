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
    Helper parameters to create a park.
    """
    latitude = base_fields.Float(
        validate=validate.Range(min=-90.0, max=90.0, error="Invalid latitude parameters. Must be between -90 and 90.")
    )
    longitude = base_fields.Float(
        validate=validate.Range(min=-180.0, max=180.0,
                                error="Invalid longitude parameters. Must be between -180 and 180.")
    )
    name = base_fields.String(
        validate=validate.Range(min=0)
    )
    address = base_fields.String(
        validate=validate.Range(min=0)
    )
    operator = base_fields.String(
        validate=validate.Range(min=0)
    )
    sponsors = base_fields.List(
        cls_or_instance=base_fields.String()
    )
    opening_time = base_fields.String(
        validate=validate.Range(min=0)
    )
    closing_time = base_fields.String(
        validate=validate.Range(min=0)
    )
    admission_price = base_fields.Float(
        validate=validate.Range(min=0.0, error="Invalid price parameters. Must be greater than or equal to$0.")
    )

