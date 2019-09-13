# pylint: disable=unused-argument

from flask import current_app, request
from google.auth.transport import requests
from google.oauth2 import id_token
from werkzeug.exceptions import BadRequest, Forbidden, InternalServerError, Unauthorized


class RequireAuth:
    def __init__(self, service):
        self.available_services = [
            'google',
            'auth0',
        ]
        self.service = service
        self.user_token = None
        self.authorized_clients = None

    def __call__(self, func):
        def wrap(*args, **kwargs):
            if self.service not in self.available_services:
                raise InternalServerError('Server can not response in this moment, please try again')
            self._get_authorized_clients()
            auth_header = request.headers.get('Authorization')
            if auth_header:
                try:
                    token = auth_header.split(' ')[1]
                except IndexError:
                    raise BadRequest('Invalid Authorization header format')
                self._decode_token(token)
            else:
                raise Unauthorized()
            return func(user_token=self.user_token, *args, **kwargs)
        wrap.wrapper = self
        return wrap

    def _decode_token(self, token):
        cases = {
            'google': self._decode_google_token(token),
            'auth0': self._decode_auth0_token(token),
        }
        cases.get(self.service)

    def _decode_google_token(self, token):
        """
        Decode Google token

        Args:
            token (Str): the authorization token

        Returns:
            user_token (Dict): the decoded user token

        Raises:
            Forbidden: when the client is not authorized
            Unauthorized: when the token is expired or is invalid
        """

        self.user_token = id_token.verify_oauth2_token(token, requests.Request())
        if self.user_token['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise Unauthorized('Authorization token is invalid')
        if self.user_token['aud'] not in self.authorized_clients:
            raise Forbidden()

    def _decode_auth0_token(self, token):
        """
        Decode Auth0 token

        Args:
            token (Str): the authorization token
        """
        pass

    def _get_authorized_clients(self):
        """
        Get the authorized clients list from configuration

        Returns:
            String list of authorized clients, None if is not configured in .env file
        """

        clients = current_app.config['AUTHORIZED_CLIENTS']
        try:
            self.authorized_clients = clients.split(',')
        except IndexError:
            raise InternalServerError('Server can not response in this moment, please try again')
