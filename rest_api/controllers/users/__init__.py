# flake8: noqa
# pylint: disable=wildcard-import
from flask_restplus import Namespace


users = Namespace('users', description='Example endpoint')


from .views import *
