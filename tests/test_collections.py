import pytest
from flask import g, session
import json

def test_collections(client, app):
    response = client.get('/v1/collections/TCGA')
    assert response.status_code == 200
    response_data = response.json['collections']
    assert 'TCGA-BRCA' in response_data
