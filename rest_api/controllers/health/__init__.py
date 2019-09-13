# flake8: noqa
# pylint: disable=wildcard-import
from flask_restplus import Namespace


health = Namespace('health', description='Check the API health status')


from .views import *
