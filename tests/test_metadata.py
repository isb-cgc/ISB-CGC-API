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


def test_versions(client, app):
    response = client.get('/v1/versions')
    assert response.status_code == 200
    data = response.json['version']
    versions = {version['name']: {key: version[key] for key in version.keys() if key != 'name'} for version in data}
    assert 'GDC Data Release 9' in versions
    assert 'TCIA Image Data' in versions
    assert 'TCIA Derived Data' in versions
    assert versions['GDC Data Release 9']['version'] == 'r9'
    assert versions['TCIA Image Data']['version'] =='1'

def test_attributes(client, app):
    response = client.get('/v1/attributes')
    assert response.status_code == 200
    data = response.json['attributes']
    attributes = {attribute['name']: {key: attribute[key] for key in attribute.keys() if key != 'name'} for attribute in data}
    assert 'program_name' in attributes
    assert attributes['program_name']['dataSetTypes'][0]['data_type'] == 'Clinical, Biospecimen, and Mutation Data'
    assert attributes['program_name']['dataSetTypes'][0]['set_type'] == 'related_set'

    assert 'days_to_collection' in attributes
    assert attributes['days_to_collection']['data_type'] == 'Continuous Numeric'
    assert int(attributes['days_to_collection']['range'][0]['id']) == 25
    assert attributes['days_to_collection']['range'][0]['type'] == 'Integer'
    assert attributes['days_to_collection']['range'][0]['include_lower'] == True
    assert attributes['days_to_collection']['range'][0]['include_upper'] == False
    assert attributes['days_to_collection']['range'][0]['unbounded'] == True
    assert attributes['days_to_collection']['range'][0]['first'] == '10'
    assert attributes['days_to_collection']['range'][0]['last'] == '80'
    assert attributes['days_to_collection']['range'][0]['gap'] == '10'
    assert 'Modality' in attributes
    assert attributes['Modality']['dataSetTypes'][0]['data_type'] == 'Image Data'
    assert attributes['Modality']['dataSetTypes'][0]['set_type'] == 'origin_set'
    assert 'SegmentedPropertyCategoryCodeSequence' in attributes
    assert attributes['SegmentedPropertyCategoryCodeSequence']['dataSetTypes'][0]['data_type'] == 'Derived Data'
    assert attributes['SegmentedPropertyCategoryCodeSequence']['dataSetTypes'][0]['set_type'] == 'derived_set'
    assert attributes['SegmentedPropertyCategoryCodeSequence']['IDCVersion'][0] == 1

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
    # One collection with id == "idc_thca"
    assert len(list(filter(lambda collection: collection['collection_id'].lower() == "tcga_thca", data))) == 1
    for collection in data:
        if collection["collection_id"] == 'tcga_prad':
            assert collection['access'] == 'Public'
            assert collection['active'] == True
            assert collection['collection_id'] == "tcga_prad"
            assert collection['cancer_type']=='Prostate Cancer'
            assert collection['collection_type']=='Original'
            assert '10.7937/K9/TCIA.2016.YXOGLM4Y' in collection['doi']
            assert collection['image_types']=='CT, PT, MR, Pathology'
            assert collection['location']=='Prostate'
            assert collection['owner_id']==1
            assert collection['species']=='Human'
            assert collection['status']=='Complete'
            assert collection['subject_count']==14
            assert collection['supporting_data']=='Clinical Genomics'



# def test_programs_get_fields(client, app):
#     # Test response to a no attribute_group
#     response = client.get('/v1/programs/TCGA/TCGA-BCLA')
#     assert response.status_code == 500
#     data = response.json
#     assert data["message"] == 'An attribute_type was not specified. Collection details could not be provided.'
#     assert data["code"] == 400
#
#     query_string = {
#         'attribute_type': 'A',
#         'version': 'r9'
#     }
#     response = client.get('/v1/programs/TCGA/FOO',query_string = query_string)
#     assert response.status_code == 500
#     data = response.json
#     assert data["message"] == 'Collection FOO does not exist'
#
#     # Get attributes in the TCIA Image Data attribute group
#     query_string = {
#         'attribute_type': 'I',
#         'version': '0'
#     }
#     response = client.get('/v1/programs/TCGA/TCGA-BRCA',query_string = query_string)
#     assert response.status_code == 200
#     # data = json.loads(response.json['collection'])
#     data = response.json['collection']
#     assert 'TCGA-BRCA' == data["collection_name"]
#     assert len(list(filter(lambda field: field['name'] == "Modality", data['fields']))) == 1
#
#     # Get attributes in the BioClin attribute group
#     query_string = {
#         'attribute_type': 'A',
#         'version': 'r9'
#     }
#     response = client.get('/v1/programs/TCGA/TCGA-BRCA',query_string = query_string)
#     assert response.status_code == 200
#     data = response.json['collection']
#     assert 'TCGA-BRCA' == data["collection_name"]
#     assert len(list(filter(lambda field: field['name'] == "program_name", data['fields']))) == 2
#     assert len(list(filter(lambda field: field['name'] == "min_percent_tumor_nuclei", data['fields']))) == 1
#     assert len(list(filter(lambda field: field['name'] == "person_neoplasm_cancer_status", data['fields']))) == 1
#
#     # Test that an invalid version is recognized
#     query_string = {
#         'attribute_type': 'A',
#         'version': 'r8'
#     }
#     response = client.get('/v1/programs/TCGA/TCGA-BRCA',query_string = query_string)
#     assert response.status_code == 500
#     data = response.json
#     assert data["message"] == 'Attribute type/version A/r8 does not exist'
#
#     # Test that the attributes of the active attribute_group are returned
#     query_string = {
#         'attribute_type': 'A'
#     }
#     response = client.get('/v1/programs/TCGA/TCGA-BRCA',query_string = query_string)
#     assert response.status_code == 200
#     data = response.json['collection']
#     assert data["version"] == "r9"
#
#     query_string = {
#         'attribute_type': 'I'
#     }
#     response = client.get('/v1/programs/TCGA/TCGA-BRCA',query_string = query_string)
#     assert response.status_code == 200
#     data = response.json['collection']
#     assert data["version"] == "0"
