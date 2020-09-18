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

import json


def test_get_programs_collections(client, app):
    response = client.get('/v1/programs/TCGA')
    assert response.status_code == 200
    data = response.json['collections']
    # One collection with id == "idc_thca"
    collections = {collection['collection_id']: {key: collection[key] for key in collection.keys() if key != 'collection_id'} for collection
                in data}
    assert 'tcga_prad' in collections

    assert len(list(filter(lambda collection: collection['collection_id'].lower() == "tcga_thca", data))) == 1
    collection = collections['tcga_prad']
    assert collection['active'] == True
    assert collection['cancer_type']=='Prostate Cancer'
    assert collection['collection_type']=='Original'
    assert '10.7937/K9/TCIA.2016.YXOGLM4Y' in collection['doi']
    assert collection['image_types']=='CT, PT, MR, Pathology'
    assert collection['location']=='Prostate'
    assert collection['species']=='Human'
    assert collection['subject_count']==14
    assert collection['supporting_data']=='Clinical Genomics'
    assert collection['IDC_versions'] == ["1.0"]

    response = client.get('/v1/programs/ISPY')
    assert response.status_code == 200
    data = response.json['collections']
    # One collection with id == "idc_thca"
    collections = {collection['collection_id']: {key: collection[key] for key in collection.keys() if key != 'collection_id'} for collection
                in data}
    assert 'ispy1' in collections

    assert len(list(filter(lambda collection: collection['collection_id'].lower() == "ispy1", data))) == 1
    collection = collections['ispy1']
    assert collection['active'] == True
    assert collection['cancer_type']=='Breast Cancer'
    assert collection['collection_type']=='Original'
    assert '10.7937/K9/TCIA.2016.HdHpgJLK' in collection['doi']
    assert collection['image_types']=='MR, SEG'
    assert collection['location']=='Breast'
    assert collection['species']=='Human'
    assert collection['subject_count']==222
    assert collection['supporting_data']=='Clinical, Image Analyses'
    assert collection['IDC_versions'] == ["1.0"]

def test_versions(client, app):
    response = client.get('/v1/versions')
    assert response.status_code == 200
    data = response.json['versions']
    versions = {version['version_number']: {key: version[key] for key in version.keys() if key != 'version_number'} for version in data}
    assert len(versions) == 1
    assert "1.0" in versions
    assert versions["1.0"]["active"] == True
    assert versions["1.0"]['name'] == 'Imaging Data Commons Data Release'
    assert versions["1.0"]["data_sources"] == \
           [{'name': 'idc-dev-etl.idc_tcia_views_mvp_wave0.dicom_all'}, {'name': 'isb-cgc.TCGA_bioclin_v0.Biospecimen'}, {'name': 'isb-cgc.TCGA_bioclin_v0.clinical_v1'}, {'name': 'idc-dev-etl.idc_tcia_views_mvp_wave0.segmentations'}, {'name': 'idc-dev-etl.idc_tcia_views_mvp_wave0.qualitative_measurements'}, {'name': 'idc-dev-etl.idc_tcia_views_mvp_wave0.quantitative_measurements'}]

def test_attributes(client, app):
    response = client.get('/v1/attributes')
    assert response.status_code == 200
    data = response.json['attributes']
    attributes = {attribute['name']: {key: attribute[key] for key in attribute.keys() if key != 'name'} for attribute in data}
    assert 'program_name' in attributes
    # assert attributes['program_name']['dataSetTypes'][0]['data_type'] == 'Clinical, Biospecimen, and Mutation Data'
    assert attributes['program_name']['dataSetTypes'][0] == 'Clinical, Biospecimen, and Mutation Data'
    assert 'days_to_collection' in attributes
    assert attributes['days_to_collection']['data_type'] == 'Continuous Numeric'
    assert 'Modality' in attributes
    assert attributes['Modality']['dataSetTypes'][0] == 'Image Data'
    assert 'SegmentedPropertyCategoryCodeSequence' in attributes
    assert attributes['SegmentedPropertyCategoryCodeSequence']['dataSetTypes'][0] == 'Derived Data'
    assert attributes['SegmentedPropertyCategoryCodeSequence']['idc_versions'][0] == 1

#
def test_programs(client, app):
    response = client.get('/v1/programs')
    assert response.status_code == 200
    data = response.json['programs']
    programs = {program['short_name']: {key: program[key] for key in program.keys() if key != 'short_name'} for program in data}
    assert "TCGA" in programs
    assert programs["TCGA"]["name"] == "The Cancer Genome Atlas"
    assert "ISPY" in programs
    assert len(list(filter(lambda program: program['short_name'] == "TCGA", data))) == 1
    assert len(list(filter(lambda program: program['name'] == "The Cancer Genome Atlas", data))) == 1


# def test_collections(client, app):
#
#     idc_version = 1
#     response = client.get('/v1/collections/{}'.format(idc_version))
#     assert response.status_code == 200
#     data = response.json['collections']
#     collections = {program['name']: {key: collection[key] for key in collections.keys() if key != 'name'} for collection in data}
#     assert "TCGA" in programs
