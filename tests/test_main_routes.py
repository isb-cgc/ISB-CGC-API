import pytest
from flask import g, session


def test_about(client, app):
    response = client.get('/v1/about')
    assert client.get('/v1/about').status_code == 200
    assert 'NCI IDC API' in response.json['message']

def test_help(client,app):
    response = client.get('v1/help/')
    assert response.status_code == 200
    assert "System Documentation" in response.json['data']

def test_oauth2callback(client, app):
    response = client.get('v1/oauth2callback')
    print(response)