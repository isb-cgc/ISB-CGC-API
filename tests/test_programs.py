import pytest
from flask import g, session
import json


def test_programs(client, app):
    response = client.get('/v1/programs')
    assert response.status_code == 200
    response_data = response.json['programs']
    assert 'TCGA' in response_data
    assert 'The Cancer Genome Atlas' in response_data

def test_collections_in_program(client, app):
    response = client.get('/v1/programs/TCGA')
    assert response.status_code == 200
    response_data = response.json['collections']
    assert 'TCGA-BRCA' in response_data
