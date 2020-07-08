#
# Copyright 2020, Institute for Systems Biology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


def test_programs(client, app):
    response = client.get('/v1/programs')
    assert response.status_code == 200
    data = response.json['programs']
    assert len(list(filter(lambda program: program['short_name'] == "TCGA", data))) == 1
    assert len(list(filter(lambda program: program['name'] == "The Cancer Genome Atlas", data))) == 1


def test_programs_get_collections(client, app):
    response = client.get('/v1/programs/TCGA')
    assert response.status_code == 200
    data = response.json['collections']
    # One collection with short_name == "thca"
    assert len(list(filter(lambda collection: collection['short_name'].lower() == "thca", data))) == 1
    # One collection with name == "TCGA-STAD"
    assert len(list(filter(lambda collection: collection['name'] == "TCGA-STAD", data))) == 1
    for collection in data:
        if collection['name'] == "TCGA-STAD":
            len(list(filter(lambda dv: dv['version'] =='r9' and dv['name'] == 'TCGA_Clinical_and_Biospecimen_Data' and dv['data_type'] == 'A', collection['data_version']))) == 1



def test_programs_get_fields(client, app):
    # Test response to a no attribute_group
    response = client.get('/v1/programs/TCGA/TCGA-BCLA')
    assert response.status_code == 500
    data = response.json
    assert data["message"] == 'An attribute_type was not specified. Collection details could not be provided.'
    assert data["code"] == 400

    query_string = {
        'attribute_type': 'A',
        'version': 'r9'
    }
    response = client.get('/v1/programs/TCGA/FOO',query_string = query_string)
    assert response.status_code == 500
    data = response.json
    assert data["message"] == 'Collection FOO does not exist'

    # Get attributes in the TCIA Image Data attribute group
    query_string = {
        'attribute_type': 'I',
        'version': '0'
    }
    response = client.get('/v1/programs/TCGA/TCGA-BRCA',query_string = query_string)
    assert response.status_code == 200
    # data = json.loads(response.json['collection'])
    data = response.json['collection']
    assert 'TCGA-BRCA' == data["collection_name"]
    assert len(list(filter(lambda field: field['name'] == "Modality", data['fields']))) == 1

    # Get attributes in the BioClin attribute group
    query_string = {
        'attribute_type': 'A',
        'version': 'r9'
    }
    response = client.get('/v1/programs/TCGA/TCGA-BRCA',query_string = query_string)
    assert response.status_code == 200
    data = response.json['collection']
    assert 'TCGA-BRCA' == data["collection_name"]
    assert len(list(filter(lambda field: field['name'] == "program_name", data['fields']))) == 2
    assert len(list(filter(lambda field: field['name'] == "min_percent_tumor_nuclei", data['fields']))) == 1
    assert len(list(filter(lambda field: field['name'] == "person_neoplasm_cancer_status", data['fields']))) == 1

    # Test that an invalid version is recognized
    query_string = {
        'attribute_type': 'A',
        'version': 'r8'
    }
    response = client.get('/v1/programs/TCGA/TCGA-BRCA',query_string = query_string)
    assert response.status_code == 500
    data = response.json
    assert data["message"] == 'Attribute type/version A/r8 does not exist'

    # Test that the attributes of the active attribute_group are returned
    query_string = {
        'attribute_type': 'A'
    }
    response = client.get('/v1/programs/TCGA/TCGA-BRCA',query_string = query_string)
    assert response.status_code == 200
    data = response.json['collection']
    assert data["version"] == "r9"

    query_string = {
        'attribute_type': 'I'
    }
    response = client.get('/v1/programs/TCGA/TCGA-BRCA',query_string = query_string)
    assert response.status_code == 200
    data = response.json['collection']
    assert data["version"] == "0"
