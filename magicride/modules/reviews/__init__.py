from magicride.extensions.api import api_v1


def init_app(app, **kwargs):
    # pylint: disable=unused-argument,unused-variable
    """
    Init reviews module.
    """
    # Touch underlying modules
    from . import models, resources

    api_v1.add_namespace(resources.reviews_ns)
