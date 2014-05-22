# -*- coding: utf-8 -*-
"""
  flask.ext.sparapi
  ~~~~~~~~~~~~~~~~~

  Flask-Sparapi is a Flask extension that aims to add a fast and simple way
  to secure API for Flask applications.

  :copyright: (c) 2014 by Sovanna Hing.
  :license: BSD (3-Clause) License, see LICENSE for more details.
"""

__version__ = '1.0.0'

from functools import wraps
import base64
import hmac
import time
import hashlib
import flask
import utils
import datastore

_default_config = {
  'KEY': '526ef54842794a8d8baa5532a3ba84e5',
  'SECRET': 'd122093ef28a411a91704abfbb9a370c',
  'HEADER_KEY': 'SparaAuthKEY',
  'HEADER_SIGNED': 'SparaAuthSIGNED',
  'CACHE_ROOT_KEY': 'SparaCacheRoot'
}

class Sparapi(object):

  def __init__(self, app=None):
    self.app = app
    if app is not None:
      self.init_app(app)


  def init_app(self, app):
    for key, value in _default_config.items():
      app.config.setdefault('SPARAPI_' + key, value)

    with app.app_context():
      try:
        if 'REDIS_HOST' in self.app.config:
          host = self.app.config['REDIS_HOST']
        else:
          host = 'localhost'
        self.cRedis = datastore.ConnecterRedis(host=host)
      except Exception, e:
        raise e

      self.cRedis.set_consumer(utils.config_value('KEY'),\
                               utils.config_value('SECRET'))

      @flask.current_app.before_request
      def per_request_callbacks():
        """Part of FLASK SNIPPETS 53 http://flask.pocoo.org/snippets/53/
        Allows to call function only after a specific request and not all.
        """
        for func in getattr(flask.g, 'sparapi_call_before_request', ()):
          func()


  def before_this_request(func):
    """Part of FLASK SNIPPETS 53 http://flask.pocoo.org/snippets/53/
    Allows to call function only after a specific request and not all.
    """
    if not hasattr(flask.g, 'sparapi_call_before_request'):
      flask.g.sparapi_call_before_request = []
    flask.g.sparapi_call_before_request.append(func)
    return func


  def secure(self, func):
    """Decorator that protect endpoint by using simple
    process checking key/secret.
    """
    @wraps(func)
    def decorated(*args, **kwargs):
      """Check if the request is authorized"""
      request = flask.request
      abort = flask.abort

      if request.method != 'POST': abort(405)

      key = request.headers.get(utils.config_value('HEADER_KEY'), None)
      if key is None: abort(417)

      message = request.headers.get(utils.config_value('HEADER_SIGNED'), None)
      if message is None: abort(417)

      consumer_secret = self.cRedis.get_consumer_secret(key)
      if consumer_secret is None: abort(400)

      if not isinstance(request.data, str): abort(400)
      hashed = hmac.new(consumer_secret.encode('utf-8'), \
                        request.data, \
                        hashlib.sha1).hexdigest()
      signed = base64.b64encode(hashed)
      if message != signed: abort(401)

      data = flask.json.loads(request.data)
      if not 'nonce' in data: abort(400)
      nonce = self.cRedis.get_nonce(key)
      if nonce is None: abort(400)
      if float(data['nonce']) > float(nonce):
        try:
          self.cRedis.set_nonce(key, '%.6f' % time.time())
        except Exception, e:
          print e
          abort(401)
      
      return func(*args, **kwargs)
    return decorated


  def new_consumer(self, key, secret):
    """Define a new consumer with key and secret
    
    :param key: The consumer KEY
    :param secret: The consumer SECRET
    """
    self.cRedis.set_consumer(key, secret)
    return dict(key=key, secret=self.cRedis.get_consumer_secret(key))