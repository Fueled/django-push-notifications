# encoding: utf-8
from setuptools import setup, find_packages

setup(
    name='django-push-notifications',
    version='0.1.0',
    author=u'Paul Oostenrijk',
    author_email='paul@glemma.nl',
    packages=find_packages(),
    url='https://github.com/Fueled/django-push-notifications',
    description='Push notification wrapper for Django',
    #long_description=open('README.txt').read(),
    install_requires=['requests'],
    zip_safe=False,
)
