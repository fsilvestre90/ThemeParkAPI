
def init_app(app, **kwargs):
    # pylint: disable=unused-argument,unused-variable
    """
    Init bookmarks module.
    """
    # Touch underlying modules
    from . import models
