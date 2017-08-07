# pylint: disable=too-few-public-methods,invalid-name,missing-docstring
import os


class BaseConfig(object):
    SECRET_KEY = 'securepassword'
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = 'postgresql:///magicride'

    DEBUG = False
    ERROR_404_HELP = False

    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

    CSRF_ENABLED = False

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    ENABLED_MODULES = (
        'parks',
        'users',
        'api',
    )


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass
