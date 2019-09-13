from rest_api import create_api, db
import rest_api.models


api = create_api()
# Makes compatible with Passenger WSGI servers
application = api

if __name__ == "__main__":
    api.run()
