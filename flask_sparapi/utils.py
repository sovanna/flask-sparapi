# -*- coding: utf-8 -*-
"""
  flask.ext.sparapi.utils
  ~~~~~~~~~~~~~~~~~~~~~~~

  Flask-Sparapi utils module.

  :copyright: (c) 2014 by Sovanna Hing.
  :license: BSD (3-Clause) License, see LICENSE for more details.
"""

from flask import current_app


def get_config(app):
    """Conveniently get the sparapi configuration for the specified
    application without the annoying 'SPARAPI_' prefix.

    :param app: The application to inspect
    """
    items = app.config.items()
    prefix = 'SPARAPI_'

    def strip_prefix(tup):
        return (tup[0].replace('SPARAPI_', ''), tup[1])

    return dict([strip_prefix(i) for i in items if i[0].startswith(prefix)])


def config_value(key, app=None, default=None):
    """Get a Flask-Sparapi configuration value.

    :param key: The configuration key without the prefix `SPARAPI_`
    :param app: An optional specific application to inspect.
                Defaults to Flask's `current_app`
    :param default: An optional default value if the value is not set
    """
    app = app or current_app
    return get_config(app).get(key.upper(), default)
