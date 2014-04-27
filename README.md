flask-sparapi
=============

[![Build Status](https://magnum.travis-ci.com/sovanna/flask-sparapi.svg?token=qzFu9Qfosru1rcm6YHB5&branch=master)](https://magnum.travis-ci.com/sovanna/flask-sparapi)

A fast and simple way to secure API for Flask applications

Resources
---------

- [Documentation](http://packages.python.org/Flask-Sparapi) (coming soon)
- [Issue Tracker](https://github.com/sovanna/flask-sparapi/issues)
- [Source](https://github.com/sovanna/flask-sparapi)
- [Development Version](https://github.com/sovanna/flask-sparapi/raw/develop#egg=Flask-Sparapi-dev)

Install
-------

python setup.py install


Usage
-----

There is a `test_app` in `test` folder.
Basically, just import and initialize it, then use the decorator `sparapi.secure`

	from flask_sparapi import Sparapi
	sparapi = Sparapi(app)
	
	@app.route('/', methods=['POST'])
	@sparapi.secure
	def index():
	  return flask.jsonify(result='success')


Additional Notes
----------------

This is the first time that i try to develop a flask extension.
Flask-Sparapi is not the greatest thing but it was interesting for me.
Now, something more bigger will coming out in the next few months..
(another great, usefull and lovely extension called Flask-......)

-_- this is a secret