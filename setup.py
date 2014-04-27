"""
Flask-Sparapi
==============

Flask-Sparapi is a Flask extension that aims to add a fast and simple way
to secure API for Flask applications.

Resources
---------

- [Documentation](http://packages.python.org/Flask-Sparapi) (coming soon)
- [Issue Tracker](https://github.com/sovanna/flask-sparapi/issues)
- [Source](https://github.com/sovanna/flask-sparapi)
- [Development Version](https://github.com/sovanna/flask-sparapi/raw/develop#egg=Flask-Sparapi-dev)

"""

from setuptools import setup

setup(
  name='Flask-Sparapi',
  version='1.0.0',
  url='https://github.com/sovanna/flask-sparapi',
  license='BSD (3-Clause) License',
  author='Sovanna Hing',
  author_email='sovanna.hing@gmail.com',
  description='Fast and simple way to secure API for Flask apps',
  long_description=__doc__,
  packages=['flask_sparapi'],
  zip_safe=False,
  include_package_data=True,
  platforms='any',
  install_requires=[
    'Flask>=0.10.1',
    'redis>=2.9.1'
  ],
  classifiers=[
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ]
)
