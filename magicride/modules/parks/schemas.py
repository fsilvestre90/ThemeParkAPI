# encoding: utf-8
"""
Serialization schemas for Park resources RESTful API
----------------------------------------------------
"""

from magicride.extensions import db
from magicride.modules.parks.models import Park
from magicride.modules.parks.serializers import GeographySerializer, OperatorSerializer, \
                                                BusinessHoursSerializer, GeoConverter
from utilities import ModelSchema


class BaseParkSchema(ModelSchema):
    location = GeographySerializer(attribute='location')
    operator = OperatorSerializer(attribute='operator')
    business_hours = BusinessHoursSerializer(attribute='business_hours')

    class Meta:
        model = Park
        sqla_session = db.session
        model_converter = GeoConverter
