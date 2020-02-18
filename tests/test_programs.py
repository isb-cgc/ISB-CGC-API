import json


def test_programs(client, app):
    response = client.get('/v1/programs')
    assert response.status_code == 200
    data = json.loads(response.json['programs'])
    assert len(list(filter(lambda program: program['short_name'] == "TCGA", data))) == 1
    assert len(list(filter(lambda program: program['name'] == "The Cancer Genome Atlas", data))) == 1


def test_programs_get_collections(client, app):
    response = client.get('/v1/programs/TCGA')
    assert response.status_code == 200
    data = json.loads(response.json['collections'])
    # One collection with short_name == "thca"
    assert len(list(filter(lambda collection: collection['short_name'].lower() == "thca", data))) == 1
    # One collection with name == "TCGA-STAD"
    assert len(list(filter(lambda collection: collection['name'] == "TCGA-STAD", data))) == 1
    for collection in data:
        if collection['name'] == "TCGA-STAD":
            len(list(filter(lambda dv: dv['version'] =='r9' and dv['name'] == 'TCGA_Clinical_and_Biospecimen_Data' and dv['data_type'] == 'A', collection['data_version']))) == 1



def test_programs_get_fields(client, app):
    query_string = {
        'attribute_group': 'TCIA Image Data',
        'version': '0'
    }
    response = client.get('/v1/programs/TCGA/BRCA',query_string = query_string)
    assert response.status_code == 200
    data = json.loads(response.json['collection'])
    assert 'BRCA' == data["collection_name"]
    assert len(list(filter(lambda field: field['name'] == "Modality", data['fields']))) == 1

    query_string = {
        'attribute_group': 'TCGA Clinical and Biospecimen Data',
        'version': 'r9'
    }
    response = client.get('/v1/programs/TCGA/BRCA',query_string = query_string)
    assert response.status_code == 200
    data = json.loads(response.json['collection'])
    assert 'BRCA' == data["collection_name"]
    assert len(list(filter(lambda field: field['name'] == "program_name", data['fields']))) == 2
    assert len(list(filter(lambda field: field['name'] == "min_percent_tumor_nuclei", data['fields']))) == 1
    assert len(list(filter(lambda field: field['name'] == "person_neoplasm_cancer_status", data['fields']))) == 1

    query_string = {
        'attribute_group': 'TCGA Clinical and Biospecimen Data',
        'version': 'r8'
    }
    response = client.get('/v1/programs/TCGA/BRCA',query_string = query_string)
    assert response.status_code == 200
    data = json.loads(response.json['collection'])
    assert data["message"] == 'Attribute group/version TCGA Clinical and Biospecimen Data/r8 does not exist'

    query_string = {
        'attribute_group': 'TCGA Clinical and Biospecimen Data',
        'version': 'r9'
    }
    response = client.get('/v1/programs/TCGA/FOO',query_string = query_string)
    assert response.status_code == 200
    data = json.loads(response.json['collection'])
    assert data["message"] == 'Program/collection TCGA/FOO does not exist'
