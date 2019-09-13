# REST API python base project

This base project contains the following preinstallation and configuration to create a Python REST API project:

* Python 3.6.8
* Support different environments and set API version sufix automaticaly
* Flask-RestPlus project fully configured with MySQL database with migrations using FlaskMigrate, ORM using SQLAlchemy, rate limits using Flask-Limiter and JWT authentication using google-auth
* Custom API information in documentation page
* Support Passenger WSGI entry point for different hosting providers
* Ready for  API documentation
* Ready for unit and functional tests
* Ready for virtual environments using pyenv or virtualenv and make

# Installation
## Prepare your local environment
### Cloning repository

First clone this repository to your local environment, also you can create a new fork and work with it:

```ssh
  $ git clone https://github.com/parisbs/rest-api-python-base-project [yourproject-name]
```

### Set the .env file

When you have the code in your local environment copy and rename the .env.example to .env and edit the values of all environment variables, here are a little description about each one:

* ENV (String): environment to run, you can set dev|prod|test
* MYSQL_HOST (String): address to your MySQL server
* MYSQL_USER (String): user to login in MySQL
* MYSQL_PASSWORD (String): password for the MySQL user
* MYSQL_DATABASE (String): name of the database for the project in MySQL
* MYSQL_CHARSET (String): charset to use in MySQL connections and tables, recommended UTF8MB4
* API_NAME (String): name to show in API documentation
* API_VERSION (Integer): version to show in API documentation and in the URIs, always prefixed by 'v', e.g. my-api.com/v1/hello, recommended only numbers but you could use another URL encode compatible characters, you can hide the version in URIs with SHOW_VERSION_URI variable
* API_DESCRIPTION (String): description to show in API documentation
* API_PORT (Integer): port to use with your API, default is 80
* API_DOCUMENTATION (String): URI for API documentation, you can set to blank if you want to show the docs in your index page, e.g. value docs to use my-api.com/v1/docs and blank value to use my-api.com/v1 to show the API documentation, the variable SHOW_VERSION_URI also affect this URLs
* AUTHOR_NAME (String): name of the API author
* AUTHOR_EMAIL (String): email of the API author
* AUTHOR_URL (String): URL to author web page or project web page
* SHOW_VERSION_URI (Boolean): if you want to show the version indicator in URIs
* AUTHORIZED_CLIENTS (String): list separated with commas and without spaces of the authorized clients for JWT authorizations
* RATELIMIT_ENABLED (Boolean): if rate limits will be enabled or disabled
* RATELIMIT_DEFAULT (String): rules for rate limits separated with commas (,) or semicolons (;), consider that values asigned in decorators will override this values
* RATELIMIT_HEADERS_ENABLED (Boolean): if rate limits headers will show in any response or not
* RATELIMIT_KEY_PREFIX (String): prefix for keys to use in rates storage, recommended when you have a shared hosting service

### Install Virtualenv or Pyenv

Now you need Virtualenv or Pyenv to install and prepare your environment, show how to install it in your OS in the following links:

* Virtualenv for Windows, Linux and Mac you can use PIP, [see how][virtualenv]
* Pyenv for Windows, Linux and Mac you can see the installation manual [here][pyenv]

When you already have any wrapper installed create a new environment using python 3.6.8 and activate it, if is necessary create your .python-version file:

```ssh
$ # If you use Pyenv
  $ echo "your_environment_name" > .python-version
  $ pyenv activate
  $ # If you use Virtualenv
  $ source [your_environment_name]/bin/activate
```

### Install dependencies and database

Install all the project dependencies, create new user and database in MySQL and run the tests to verify taht's all right

```ssh
  $ make install
  $ mysql.server start
  $ # Use your MySQL credentials and remove the -p if you do not set your MySQL password yet
  $ mysql -u root -p
  $ mysql> create database rest_api;
  $ mysql> create database rest_api_test;
  $ mysql> create user 'rest_api'@'%' IDENTIFIED BY 'rest_api';
  $ mysql> grant all privileges on rest_api.* to 'rest_api'@'%';
  $ mysql> grant all privileges on rest_api_test.* to 'rest_api'@'%';
  $ mysql> exit
  $ make db-upgrade
  $ make unit-tests
```

All the tests should be passed, if not please verify if you have your python environment activated or all the dependencies were installed correctly, then try again

### Run the project

You can see the project working with the following command and visiting the following links:

```ssh
  $ make run
```

* Health endpoint: http://localhost/v1-dev/health
* Users endpoint: http://localhost/v1-dev/users/{user_id}
* API documentation: http://localhost/v1-dev/docs

The users endpoint requires authentication, you can skip this commenting the lines 24, 31 and 33 in the file rest_api/controllers/users/views.py, also delete the user_token parameter in the function at line 25:

```python
    @users.doc('Get user')
    @users.response(400, 'Invalid ID format')
    @users.marshal_with(user_model)
    """@RequireAuth('google')"""
    def get(self, user_id):
        regex = re.compile(r'^[0-9]+$')
        if not regex.match(user_id):
            raise BadRequest('Invalid ID format in your query')
        user = db.session.query(User).get(user_id)
        if user:
            """if user_id == user_token.get('sub', None):"""
            return user
            """raise Forbidden()"""
        raise Unauthorized('The authenticated user no exists')
```

You need to create an user manually to test the 200 response code in your browser

## About the project directories

In the root path of the project you can find some configuration and extra files

* .coveragerc: configuration for Coverage
* .editorconfig: configuration for the code style
* .env.example: example for environment variables file, recommend to copy and rename the copy to avoid missing variables
* .gitignore: list of git ignored files and directories
* .htaccess.example: example of htaccess file for Passenger configuration for hosting services
* config.py: configuration file to support multiple environments
* LICEnSE: License protection for the code
* Makefile: make commands file
* myapp.py: create Flask instance to use it with Passenger servers
* passenger_wsgi.py: Passenger script to run the API
* PULL_REQUEST_TEMPLATE.md: template for pull requests in GitHub
* README.md: this readme file
* requirements.txt: list of dependencies for the project
* tox.ini: configuration for Tox module for testing, linters and coverage

### rest_api directory

In this directory you can find the main api module and the __init__ file:

* api.pi: create the api instance to run with gunicorn
* __init__.py: initialize and configure the Flask instance with all the namespaces

#### controllers directory

Here you can set your namespaces directories and register them in __init__ file:

* __init__.py: import and register all the available namespaces to use in your flask API

##### health and users directories

In these paths you can put your python code for each endpoint and method:

* __init.py: create the namespace for your endpoint
* views.py: create the endpoint class and the methods behavior

#### models directory

Here you can add all your data models for SQLAlchemy, recommend to inheritance from base class

* __init__.py: import all the models
* [model_files].py: define your SQLAlchemy models

#### schemas directory

Storage all the schemas for your SQLAlchemy models to serialize them in responses

* __init__.py: required to register new python module
* [shema_files].py: define your schemas using flask_restplus.fields

#### Utils directory

Here you can add any extra util for your API

* __init__.py: required to register new python module
* [util_files].py: optional if you want to create your utils in this directory directly
* [utils_directories]/: separate your utils by directories

##### decorators directory

In this path you can add your decorators

* authentication.py: the require_auth decorator to allows JWT authorization in your endpoints

### migrations directory

Here you can configure your migration scripts template and your migration scripts for Flask-Migrate

* alembic.ini: the migration configuration
* env.py: script to auto generate your database migrations
* script.py.mako: template for your migration scripts

#### versions directory

Storage all your migration scripts for your database

* [%year%-%month%-%day%_%slug%].py: migration script file with your MySQL sentences and definitions

### tests

All the tests for the project

* __init__.py: required to register new python module

#### functional directory

For all your functional tests

* __init__.py: require to register new python module
* [test_files.py|tests_directories|utils_directories_or_files.py]: for your functional tests

#### unit

Storage your unit tests for the project

* __init__.py: required to register new python module
* conftest.py: configuration, fixtures and mocks for your tests
* [test_files].py: unit tests for your endpoints or utils

##### factories

Here you can create your SQLAlchemy factories to poblate your tables and prepare fake data in your database

* __init__.py: required to register new python module
* [factory_files].py: your factory definitions

### .github directory

Here you can add templates for GitHub issues and more

#### ISSUE_TEMPLATE directory

Storage the issues template to use in GitHub

* bug_report.md: template for report issues

### git-hooks

In this path you can add your custom git hooks

* pre-commit: git hook to run tests before commit changes

## How the project works?

The project uses factory-boy, Flask-Limiter, Flask-Migrate, flask-restplus, Flask-SQLAlchemy, google-auth, gunicorn, PyMySQL, pytest, python-dotenv, requests, tox and virtualenv

First create a Flask instance and configure it using the config.py file, this script retrieve the configuration variables from .env file; after create a flask_restplus.api instance and configure the API with the app configuration, then register the namespaces using the list in rest_api/controllers/__init__.py file where you add your new endpoints and controllers. Finaly the app run using Gunicorn or Passenger and listening HTTP requests

## How to create new namespace

Each namespace represents new endpoint for the API, to create new one follow these steps:

1. Create the controller directory in controllers path and create a new __init__.py file inside
2. Now create the file views.py and coding the functions for each method for the endpoint, you can see example the code in health and users controllers, go to the [flask-restplus documentation][namespaces] for more information about namespaces
3. Add the namespace declaration in your __init__.py file, you can see how in __init__.py files of health or users controllers
4. Finaly import your namespace of your controller (__init__.py) to the __init__.py file of the controllers module and add it to the namespaces list

## How to create new model

This project uses SQLAlchemy models to support ORM functions, you can add your models in the path rest_api/models following these steps:

1. Create a file for your model
2. Inside the file create a new class that's inheritance from Base model class or db.Model class, if you use Base model class your model automaticaly add created_at and updated_at columns in your model tables
3. Declare the name of your model table using the variable __tablename__, you can set different options and configurations for your model, go to the [SQLAlchemy documentation][models] for more information
4. Add your columns in your model and specify the data type, length if is necessary and if is nullable or not, see the SQLAlchemy documentation for more parameters
5. Add your class to __init__.py of models module

## How to create new schema

To parse the responses flask-restplus uses marchal schemas, you can add your data schemas in the path rest_api/schemas, follow these steps:

1. Create new schema file and add new variable with a dictionary defining all the keys and values for the data, uses the flask_restplus.fields to determine the data type for each key in the schema, go to the [flask-restplus documentation][fields] for more information about marshal schemas and fields
2. Add your schema variables in the __init__.py file of the schemas module

## How to use @requires_auth decorator

Right now this decorator only supports Google authentication but it's ready to work with differents authentication services, you have a unfunctional example of how to add new service in the rest_api/utils/decorators/authentication.py file as auth0

### Authenticate using Google

To authenticate users using Google you must have the authentication feature in your front-end or client app, this decorator only verify and authenticate the JWT generated when the user is successful logged in your client app using Google authentication service

When you have the authentication token for your users you need to attach it to the API calls that uses this decorator, just add to the request header the key Authorization and set the value to Bearer [user_token], then make the call and the API will process the header before the endpoint function

In your code add the decorator @RequiresAuth() with the parameter service as string where you indicate the authorization service that you want to use, also you need to add user_token as parameter in your function, this parameter will receive a dictionary with all the info of the token like issuer, subject, audience and more depending the service you use. Then you can process the user_token information to determine the actions to the endpoint like retrieve a user from db or verify some items for the user, e.g.

```python
  from rest_api.utils.decorators.authentication import RequiresAuth

  @namespace.route('/auth')
  @RequiresAuth('google')
  def get(self, user_token):
    """Do something with user_token dictionary"""
    user = db.session.query(User).get(user_token['sub'])
    if user:
      return user
```

If you want to bring access to 3rd party servers or clients you can add the Google audience ID of the external client to your AUTHORIZED_CLIENTs variable in .env file, remember separate with commas and do not use spaces between each client ID. Do not forget to add your own client ID to this variable or the API will responses with a 401 error code or 500 if you do not set the AUTHORIZED:CLIENTS variable. Go to the [Google authenticate with a backend server documentation][googleauthentication] for more information about the content of user_token and how it works

## Rate limits

This project supports rate limits for endpoints using Flask-Limiter, you can configure rate limit behavior in .env file, go to [Flask Limiter documentation][limiter] for more info about the available environment variables

### Rate limits configuration

By default this project only declared the following options:

* RATELIMIT_ENABLED (Boolean): if rate limits will be enabled or disabled
* RATELIMIT_DEFAULT (String): rules for rate limits separated with commas (,) or semicolons (;), consider that values asigned in decorators will override this values
* RATELIMIT_HEADERS_ENABLED (Boolean): if rate limits headers will show in any response or not
* RATELIMIT_KEY_PREFIX (String): prefix for keys to use in rates storage, recommended when you have a shared hosting service

### Rate limits decorators

You can set a custom rate limit for specific endpoint using the @limiter.limit() decorator, also you can exempt any endpoint using the @limiter.exemp() decorator, just import rest_api.limiter module to use it as decorator. Go to the [Flask Limiter documentation][limiter] for more information about the available decorators and parameters

## How to create new migration script

The project uses Flask-Migrate to generate database migration scripts to make easier the database management, follow these steps to create a new one:

1. Be sure that your new models are ready and have all the parameters and configurations to production, also verify that your MySQL server is running
2. Run the command `make db-migrate message='short migration description'`, the message parameter is required
3. Go to the new migration file generated in migrations/versions/ path and verify that's all right, modify the code if is necessary
4. Run the command `make db-upgrade` to apply the changes to the database
5. Also you can undo migrations using the command `make db-downgrade` with the optional parameter revision where you must pass the revision ID of the target migration file to downgrade

## Passenger servers

This project supports Passenger servers, verify if your hosting provider support python apps and Passenger controller before use this feature

You can configure your Passenger instance using the .htaccess file, copy and rename the .htaccess.example file to know what variables you must set to work, some providers can generate automaticaly the .htaccess file, verify if your provider support this feature or go to your cPanel and verify if you have a section called Python apps

## Warning

Please change MySQL configuration values to prevent attacks, I'm not responsible for any situation of theft or loss of data derived from the lack of attention to this warning

You can change the name of the main module rest_api, if you do this please remember change all the imports and scripts taht use this module to prevent issues and exceptions

## License

This project is under the MIT license so you can use, modify, share and make merchant services with this code, see the LICENSE file for more information

## Colaboration

You can colaborate to make this project better, just following these recommendations:

* Do not deactivate linters and other unit tests to commit your changes
* Use the pull request template to provide information about your changes
* Be clear in your pr explaination
* Create the functional or unit tests for your features
* Comment the functions and classes if is necessary, specialy in complex code
* To create a new pull request first fork the project and make your changes in the fork
* Follow the GitFlow pattern for your branches and make your pr to develop branch

[virtualenv]: https://virtualenv.pypa.io/en/stable/installation/
[pyenv]: https://github.com/pyenv/pyenv
[namespaces]: https://flask-restplus.readthedocs.io/en/stable/_modules/flask_restplus/namespace.html
[models]: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
[fields]: https://flask-restplus.readthedocs.io/en/stable/_modules/flask_restplus/fields.html
[googleauthentication]: https://developers.google.com/identity/sign-in/android/backend-auth
[limiter]: https://flask-limiter.readthedocs.io/en/stable/
