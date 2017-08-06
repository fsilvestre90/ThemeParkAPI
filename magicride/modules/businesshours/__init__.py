from magicride.extensions.api import api_v1


def init_app(app, **kwargs):
    # pylint: disable=unused-argument,unused-variable
    """
    Init parks module.
    """
    # Touch underlying modules
    from . import models
