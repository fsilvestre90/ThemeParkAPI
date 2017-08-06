from geoalchemy2 import Geometry
from marshmallow import fields
from marshmallow_sqlalchemy import ModelConverter
from sqlalchemy import func

from magicride.extensions import db
from magicride.modules.operators.models import Operator
from magicride.modules.geo.models import Location
from magicride.modules.businesshours.models import BusinessHours


class GeoConverter(ModelConverter):
    SQLA_TYPE_MAPPING = ModelConverter.SQLA_TYPE_MAPPING.copy()
    SQLA_TYPE_MAPPING.update({
        Geometry: fields.Str
    })


class OperatorSerializer(fields.Integer):
    def _serialize(self, value, attr, obj):
        if value is None:
            return value
        else:
            if attr == 'operator':
                operator = Operator.query.filter(Operator.id == value.id) \
                                         .first()
                return operator.name
            else:
                return None

    def _deserialize(self, value, attr, data):
        if value is None:
            return value
        else:
            if attr == 'operator':
                operator = Operator.query.filter(Operator.name == value.name) \
                                         .first()
                return operator.name
            else:
                return None


class GeographySerializer(fields.String):
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


class BusinessHoursSerializer(fields.Integer):
    def _serialize(self, value, attr, obj):
        if value is None:
            return value
        else:
            if attr == 'business_hours':
                return BusinessHours.query.filter(BusinessHours.id == value.id) \
                                         .first()
            else:
                return None
