from geoalchemy2 import Geometry
from marshmallow import fields
from marshmallow_sqlalchemy import ModelConverter
from sqlalchemy import func

from magicride.extensions import db
from magicride.modules.geo.models import Location


class GeoConverter(ModelConverter):
    SQLA_TYPE_MAPPING = ModelConverter.SQLA_TYPE_MAPPING.copy()
    SQLA_TYPE_MAPPING.update({
        Geometry: fields.Str
    })


class GeographySerializer(fields.String):
    def _serialize(self, value, attr, obj):
        if value is None:
            return value
        else:
            if attr == 'location':
                return {'longitude': db.session.scalar(func.ST_X(value)),
                        'latitude': db.session.scalar(func.ST_Y(value))}
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
