#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import push_notifications

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = push_notifications.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

setup(
    name='django-push-notifications-manager',
    version=version,
    description="A library for easily sending and configuring push"
                " notifications with ZeroPush and Urban Airship "
                "http://fueled.github.io/django-push-notifications",
    long_description="A library for easily sending and configuring push"
                     " notifications with ZeroPush and Urban Airship "
                     "Installation can be found on "
                     "http://fueled.github.io/django-push-notifications."
                     "Want to contribute? Go to: "
                     "https://github.com/Fueled/django-push-notifications",
    author='Paul Oostenrijk',
    author_email='paul@glemma.nl',
    url='https://github.com/Fueled/django-push-notifications',
    packages=[
        'push_notifications',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='push, notifications, manager, apns',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
