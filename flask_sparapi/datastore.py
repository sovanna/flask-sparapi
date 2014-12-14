# -*- coding: utf-8 -*-
"""
  flask.ext.sparapi.datastore
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~

  This module contains the app datastore manager.

  :copyright: (c) 2014 by Sovanna Hing.
  :license: BSD (3-Clause) License, see LICENSE for more details.
"""

import redis
import utils


class ConnecterRedis(object):

    """A simple Redis datastore for Flask apps.

    This class is a singleton.
    It allows to manage nonce and consumer key/secret
    as simple as possible.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, host='localhost', port=6379):
        self.r = redis.StrictRedis(host=host, port=port)
        self.root = '%s' % utils.config_value('CACHE_ROOT_KEY')

    def set_nonce(self, consumer_key, nonce):
        """Set nonce for a consumer.

        :param consumer_key: The consumer key for which we store the nonce
        :param nonce: The nonce to store
        """
        hkey = '%s:nonces:consumers:%s' % (self.root, consumer_key)
        return self.r.set(hkey, nonce)

    def get_nonce(self, consumer_key):
        """Return consumer's nonce.

        :param consumer_key: The consumer key for which we want the nonce
        """
        hkey = '%s:nonces:consumers:%s' % (self.root, consumer_key)
        return self.r.get(hkey)

    def set_consumer(self, key, secret):
        """Set a new consumer.

        :param key: The consumer KEY
        :param secret: The consumer SECRET
        """
        hkey = '%s:consumers:%s' % (self.root, key)
        if self.r.set(hkey, secret):
            self.set_nonce(key, 0)
            return True
        return False

    def get_consumer_secret(self, key):
        """Return consumer secret.

        :param key: The key of the consumer
        """
        hkey = '%s:consumers:%s' % (self.root, key)
        return self.r.get(hkey)
