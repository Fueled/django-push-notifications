#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import push_notifications


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]

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

readme = open('README.rst').read()

setup(
    name='django-pnm',
    version=version,
    description="""A plug and play package to handle push devices and push notifications for services such as ZeroPush and Urban Airship""",
    long_description=readme,
    author='Paul Oostenrijk',
    author_email='paul@glemma.nl',
    url='https://github.com/Fueled/django-push-notifications',
    packages=get_packages('push_notifications'),
    include_package_data=True,
    install_requires=[
        'django>=1.5.1',
        'requests>=2.5.1'
    ],
    license="BSD",
    zip_safe=False,
    keywords='pnm, django, push, notifications, manager',
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
