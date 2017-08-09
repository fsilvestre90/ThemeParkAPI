# encoding: utf-8
"""
API extension
=============
"""
from .http_exceptions import abort
from .api import Api

api_v1 = Api(  # pylint: disable=invalid-name
    version='1.0',
    title="MagicRideAPI",
    description="This API let's us monitor various theme parks, rides, and reviews.",
)


def init_app(app, **kwargs):
    pass

