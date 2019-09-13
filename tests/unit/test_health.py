def test_health_check(app):
    client = app.test_client()
    response = client.get('/v{}/health'.format(app.config['API_VERSION']))
    assert response.status_code == 200
