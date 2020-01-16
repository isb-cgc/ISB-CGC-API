import pytest
from flask import g, session


def test_about(client, app):
    response = client.get('/v1/about')
    assert client.get('/v1/about').status_code == 200
    assert 'NCI IDC API' in response.json['message']
    '''response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "select * from user where username = 'a'",
        ).fetchone() is not None
'''

def test_privacy_policy(client,app):
    response = client.get('v1/privacy/')
    assert response.status_code == 200
    assert "TemplateDoesNotExist" in response.json['data']

def test_help(client,app):
    response = client.get('v1/help/')
    assert response.status_code == 200
    assert "System Documentation" in response.json['data']

def test_oauth2callback(client, app):
    response = client.get('v1/oauth2callback')
    print(response)