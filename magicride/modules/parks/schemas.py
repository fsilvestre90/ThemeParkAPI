# encoding: utf-8
"""
Serialization schemas for Park resources RESTful API
----------------------------------------------------
"""

from magicride.extensions import db
from magicride.modules.businesshours.schemas import BaseBusinessHoursSchema
from magicride.modules.operators.schemas import BaseOperatorSchema
from magicride.modules.parks.models import Park
from magicride.modules.parks.serializers import GeographySerializer, GeoConverter
from magicride.modules.rides.schemas import BaseRideSchema
from utilities import ModelSchema
from flask_marshmallow import base_fields


class BaseParkSchema(ModelSchema):
    location = GeographySerializer(attribute='location')
    operating_hours = base_fields.Nested(BaseBusinessHoursSchema)
    operator = base_fields.Nested(BaseOperatorSchema)
    rides = base_fields.Nested(BaseRideSchema, many=True)

    class Meta:
        model = Park
        sqla_session = db.session
        model_converter = GeoConverter
        exclude = (
            Park.is_active.key,
        )


class ParkSchema(BaseParkSchema):
    rides = base_fields.Nested(BaseRideSchema, many=True)
