import pytest
from flask import g, session
import json
from time import time

# def test_collections_get_fields(client, app):
#     t = time()
#     response = client.get('/v1/collections/TCGA-BRCA/1.0')
#     print('Elapsed time: {}'.format( time()-t))
#     assert response.status_code == 200
#     response_data = response.json['collection']
#     assert 'TCGA-BRCA' == json.loads(response_data)["collection_name"]
#     assert 'program_name' in response_data
#     assert 'Modality' in response_data

