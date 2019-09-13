import re

from flask_restplus import Resource
from werkzeug.exceptions import BadRequest, Forbidden, Unauthorized

from rest_api import db
from rest_api.controllers.users import users
from rest_api.models import User
from rest_api.schemas import user_schema
from rest_api.utils.decorators.authentication import RequireAuth


user_model = users.model('User', user_schema)


@users.route('/<string:user_id>')
@users.doc(responses={404: 'Not found'})
@users.param('user_id', description='User ID', example='1')
class Users(Resource):

    @users.doc('Get user')
    @users.response(400, 'Invalid ID format')
    @users.marshal_with(user_model)
    @RequireAuth('google')
    def get(self, user_id, user_token):
        regex = re.compile(r'^[0-9]+$')
        if not regex.match(user_id):
            raise BadRequest('Invalid ID format in your query')
        user = db.session.query(User).get(user_id)
        if user:
            if user_id == user_token.get('sub', None):
                return user
            raise Forbidden()
        raise Unauthorized('The authenticated user no exists')
