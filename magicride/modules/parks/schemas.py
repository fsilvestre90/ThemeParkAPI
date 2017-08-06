# encoding: utf-8
"""
Serialization schemas for Park resources RESTful API
----------------------------------------------------
"""
from geoalchemy2 import Geometry
from marshmallow import fields
from marshmallow_sqlalchemy import ModelConverter
from sqlalchemy import func

from magicride.extensions import db
from magicride.modules.parks.models import Park, Location
from utilities import ModelSchema


class GeoConverter(ModelConverter):
    SQLA_TYPE_MAPPING = ModelConverter.SQLA_TYPE_MAPPING.copy()
    SQLA_TYPE_MAPPING.update({
        Geometry: fields.Str
    })


class GeographySerializationField(fields.String):
    def _serialize(self, value, attr, obj):
        if value is None:
            return value
        else:
            if attr == 'location':
                return {'latitude': db.session.scalar(func.ST_X(value)),
                        'longitude': db.session.scalar(func.ST_Y(value))}
            else:
                return None

    def _deserialize(self, value, attr, data):
        if value is None:
            return value
        else:
            if attr == 'location':
                return Location(value.get('longitude'), value.get('latitude'))
            else:
                return None


class BaseParkSchema(ModelSchema):
    location = GeographySerializationField(attribute='location')

    class Meta:
        model = Park
        sqla_session = db.session
        model_converter = GeoConverter
