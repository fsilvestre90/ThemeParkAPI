# encoding: utf-8
"""
Common reusable Parameters classes
----------------------------------
"""

from marshmallow import validate

from flask_marshmallow import base_fields
from utilities import Parameters


class PaginationParameters(Parameters):
    """
    Helper Parameters class to reuse pagination.
    """

    limit = base_fields.Integer(
        description="limit a number of items (allowed range is 1-100), default is 20.",
        missing=20,
        validate=validate.Range(min=1, max=100)
    )
    offset = base_fields.Integer(
        description="a number of items to skip, default is 0.",
        missing=0,
        validate=validate.Range(min=0)
    )


class FilteringParameters(Parameters):
    """
    Helper Parameters class to reuse filtering.
    """

    operator = base_fields.String(
        allow_none=True
    )
    ride_type = base_fields.List(
        cls_or_instance=base_fields.String(),
        allow_none=True
    )
    min_height_in_cm = base_fields.Integer(
        allow_none=True,
        validate=validate.Range(min=0)
    )
    admission_price = base_fields.Integer(
        allow_none=True,
        validate=validate.Range(min=0)
    )


class GeocodeParameters(Parameters):
    """
    Helper Parameters class to reuse geocoding.
    """
    search = base_fields.String(
        description="the type of query we want to search",
    )
    filters = base_fields.Raw()
    coordinates = base_fields.List(
        cls_or_instance=base_fields.List(
            cls_or_instance=base_fields.Float()
        ),
        allow_none=True,
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
