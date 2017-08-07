# encoding: utf-8
# pylint: disable=invalid-name,wrong-import-position

"""
Extensions setup
================

Extensions provide access to common resources of the application.

Put new extension instantiations and initializations here.
"""

from . import api

from sqlalchemy_utils import force_auto_coercion, force_instant_defaults

force_auto_coercion()
force_instant_defaults()

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={'autocommit': True})


def init_app(app):
    """
    Application extensions initialization.
    """

    for extension in (
            api,
            db,
    ):
        extension.init_app(app)
