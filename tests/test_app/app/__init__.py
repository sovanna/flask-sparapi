# -*- coding: utf-8 -*-
"""Main app

:copyright: (c) 2013 by Sovanna Hing.
"""

import flask
from flask_sparapi import Sparapi

"""Flask app creation"""

app = flask.Flask(__name__)
app.config.from_object('config')

"""SPARAPI"""
sparapi = Sparapi(app)

@app.route('/', methods=['POST'])
@sparapi.secure
def index():
  return flask.jsonify(result='success')