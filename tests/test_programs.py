import pytest
from flask import g, session
import json
from time import time


def test_programs(client, app):
    response = client.get('/v1/programs')
    assert response.status_code == 200
#    response_data = response.json['programs']
    data = json.loads(response.json['programs'])
    assert len(list(filter(lambda program: program['short_name'] == "TCGA", data))) == 1
    assert len(list(filter(lambda program: program['name'] == "The Cancer Genome Atlas", data))) == 1
    # assert 'TCGA' in response_data
    # assert 'The Cancer Genome Atlas' in response_data

def test_programs_get_collections(client, app):
    response = client.get('/v1/programs/TCGA')
    assert response.status_code == 200
    data = json.loads(response.json['collections'])
    assert len(list(filter(lambda collection: collection['short_name'].lower() == "thca", data))) == 1
    assert len(list(filter(lambda collection: collection['name'] == "TCGA-STAD", data))) == 1

def test_programs_get_fields(client, app):
    t = time()
    response = client.get('/v1/programs/TCGA/BRCA/1.0')
    print('Elapsed time: {}'.format( time()-t))
    assert response.status_code == 200
    data = json.loads(response.json['collection'])
    assert 'BRCA' == data["collection_name"]
    assert len(list(filter(lambda field: field['name'] == "program_name", data['fields']))) == 1
    assert len(list(filter(lambda field: field['name'] == "Modality", data['fields']))) == 1
