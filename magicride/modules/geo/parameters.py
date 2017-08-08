from marshmallow import validate

from utilities import Parameters
from flask_marshmallow import base_fields


class GeocodeParameters(Parameters):
    """
    Helper Parameters class to reuse geocoding.
    """
    search = base_fields.String(
        description="the type of query we want to search",
    )
    coordinates = base_fields.String(
        allow_none=True,
        description="the list of coordinates",
    )
    latitude = base_fields.Float(
        allow_none=True,
        description="the latitude to search in",
        validate=validate.Range(min=-90.0, max=90.0, error="Invalid latitude parameters. Must be between -90 and 90.")
    )
    longitude = base_fields.Float(
        allow_none=True,
        description="the latitude to search in",
        validate=validate.Range(min=-180.0, max=180.0,
                                error="Invalid longitude parameters. Must be between -180 and 180.")
    )
    radius = base_fields.Float(
        description="the radius to search in",
        missing=5,
        validate=validate.Range(min=0)
    )
