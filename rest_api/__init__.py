# pylint: disable=unused-argument,unused-variable
from flask import Flask
from flask_limiter import Limiter, RateLimitExceeded
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

from config import get_config_environment


db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)


def _register_namespaces(api):
    from rest_api.controllers import namespaces
    for namespace in namespaces:
        api.add_namespace(namespace)


def _register_error_handlers(api):
    @api.errorhandler(RateLimitExceeded)
    def handle_rate_limit_exceeded(error):
        data = {
            'message': 'Too many requests, verify headers for more info about current rate limits',
        }
        return data, 429


def create_api(config=None):
    app = Flask(__name__)

    if config:
        app.config.from_object(config)
    else:
        app.config.from_object(get_config_environment())

    db.app = app
    db.init_app(app)
    Migrate(app, db)

    limiter.init_app(app)

    api_version = ''
    if app.config['SHOW_VERSION_URI']:
        api_version = '/v{}'.format(app.config['API_VERSION'])
    doc_uri = '{}/{}'.format(api_version, app.config['API_DOCUMENTATION'])
    api = Api(
        app=app,
        title=app.config['API_NAME'],
        version=app.config['API_VERSION'],
        description=app.config['API_DESCRIPTION'],
        prefix=api_version,
        doc=doc_uri,
        catch_all_404s=True,
        ordered=True,
        contact=app.config['AUTHOR_NAME'],
        contact_email=app.config['AUTHOR_EMAIL'],
        contact_url=app.config['AUTHOR_URL'],
    )

    _register_namespaces(api)
    _register_error_handlers(api)

    return app
