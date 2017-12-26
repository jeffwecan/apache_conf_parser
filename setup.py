#!/usr/bin/env python
from setuptools import setup

setup(
    name='apache_conf_parser',
    version='1.0.1',
    description='Parse and manipulate apache conf files.',
    packages=['apache_conf_parser'],
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'],
)
