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
    data = response.json['versions']
    versions = {version['version_id']: {key: version[key] for key in version.keys() if key != 'version_id'} for version in data}
    assert len(versions) == 1
    assert "1" in versions
    assert len(list(filter(lambda comp: comp['name'] == 'GDC Data Release 9', versions['1']['components']))) == 1
    assert len(list(filter(lambda comp: comp['name'] == 'TCIA Image Data', versions['1']['components']))) == 1
    assert len(list(filter(lambda comp: comp['name'] == 'TCIA Derived Data', versions['1']['components']))) == 1
    assert list(filter(lambda comp: comp['name'] == 'GDC Data Release 9', versions['1']['components']))[0]['version'] == 'r9'
    assert list(filter(lambda comp: comp['name'] == 'TCIA Image Data', versions['1']['components']))[0]['version'] == '1'
    assert list(filter(lambda comp: comp['name'] == 'TCIA Derived Data', versions['1']['components']))[0]['version'] == '1'


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
