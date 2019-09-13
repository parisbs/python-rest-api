import os
from os.path import join, dirname

from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def get_config_environment():
    config = dict()
    config['prod'] = Production
    config['dev'] = Development
    config['test'] = Test
    environment = os.environ.get('ENV', 'dev').lower()
    return config.get(environment, Development)


class Config(object):
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'root')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'rest_api')
    MYSQL_CHARSET = os.environ.get('MYSQL_CHARSET', 'UTF8MB4')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_NAME = os.environ.get('API_NAME')
    API_VERSION = os.environ.get('API_VERSION', 1)
    API_DESCRIPTION = os.environ.get('API_DESCRIPTION')
    API_PORT = os.environ.get('API_PORT', 80)
    API_DOCUMENTATION = os.environ.get('API_DOCUMENTATION')
    AUTHOR_NAME = os.environ.get('AUTHOR_NAME')
    AUTHOR_EMAIL = os.environ.get('AUTHOR_EMAIL')
    AUTHOR_URL = os.environ.get('AUTHOR_URL')
    SHOW_VERSION_URI = os.environ.get('SHOW_VERSION_URI', True)
    AUTHORIZED_CLIENTS = os.environ.get('AUTHORIZED_CLIENTS')
    RATELIMIT_ENABLED = os.environ.get('RATELIMIT_ENABLED', False)
    RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT')
    RATELIMIT_HEADERS_ENABLED = os.environ.get('RATELIMIT_HEADERS_ENABLED')
    RATELIMIT_KEY_PREFIX = os.environ.get('RATELIMIT_KEY_PREFIX')
    DEBUG = False
    TESTING = False


class Production(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}?charset={}'.format(
        Config.MYSQL_USER,
        Config.MYSQL_PASSWORD,
        Config.MYSQL_HOST,
        Config.MYSQL_DATABASE,
        Config.MYSQL_CHARSET
    )


class Development(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}?charset={}'.format(
        Config.MYSQL_USER,
        Config.MYSQL_PASSWORD,
        Config.MYSQL_HOST,
        Config.MYSQL_DATABASE,
        Config.MYSQL_CHARSET
    )
    API_VERSION = '{}-dev'.format(Config.API_VERSION)
    DEBUG = True


class Test(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}_test?charset={}'.format(
        Config.MYSQL_USER,
        Config.MYSQL_PASSWORD,
        Config.MYSQL_HOST,
        Config.MYSQL_DATABASE,
        Config.MYSQL_CHARSET
    )
    TESTING = True
