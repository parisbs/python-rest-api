# pylint: disable=unused-argument
import json

from tests.unit.factories import UserFactory


def test_get_user_with_auth(app):
    client = app.test_client()
    user = UserFactory()
    path = '/v{}/users/{}'.format(app.config['API_VERSION'], user.id)
    response = client.get(path, headers={'Authorization': 'Bearer 1.2.3'})
    response_user = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert response_user['id'] == user.id
    assert response_user['name'] == user.name
    assert response_user['email'] == user.email
