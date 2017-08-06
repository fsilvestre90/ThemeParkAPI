# encoding: utf-8
"""
API extension
=============
"""
from .api import Api

api_v1 = Api(  # pylint: disable=invalid-name
    version='1.0',
    title="AnagramAPI",
    description=("This REST Api allows us to compute anagrams quickly!"),
)


def init_app(app, **kwargs):
    pass
