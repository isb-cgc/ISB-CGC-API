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
from tests.testing_config import VERSIONS, NUM_COLLECTIONS, NUM_ANALYSIS_RESULTS
from fnmatch import fnmatch


def test_versions(client, app):
    response = client.get('/v1/versions')
    assert response.status_code == 200
    data = response.json['versions']
    versions = {version['idc_data_version']: {key: version[key] for key in version.keys() if key != 'version_number'} for version in data}
    assert len(versions) == VERSIONS
    for version in range(1, VERSIONS+1):
        v = f"{version}.0"
        assert v in versions
        assert versions[v]['active'] == (version == VERSIONS)



def test_collections(client, app):

    response = client.get('/v1/collections')
    assert response.status_code == 200
    data = response.json['collections']
    collections = {collection['collection_id']: \
                   {key: collection[key] for key in collection.keys() if key != 'collection_id'} \
                   for collection in data}
    assert len(collections) == NUM_COLLECTIONS
    assert "tcga_prad" in collections
    collection = collections['tcga_prad']
    assert collection['cancer_type'] == 'Prostate Cancer'
    assert collection['description'] == '<div>\n\t<strong>Note:&nbsp;This collection has special restrictions on its usage. See <a href="https://wiki.cancerimagingarchive.net/x/c4hF" target="_blank">Data Usage Policies and Restrictions</a>.</strong></p>\n<div>\n\t&nbsp;</p>\n<div>\n\t<span>The <a href="http://imaging.cancer.gov/" target="_blank"><u>Cancer Imaging Program (CIP)</u></a></span><span>&thinsp;</span><span> is working directly with primary investigators from institutes participating in TCGA to obtain and load images relating to the genomic, clinical, and pathological data being stored within the <a href="http://tcga-data.nci.nih.gov/" target="_blank">TCGA Data Portal</a>.&nbsp;Currently this image collection of prostate adenocarcinoma (PRAD) patients can be matched by each unique case identifier with the extensive gene and expression data of the same case from The Cancer Genome Atlas Data Portal to research the link between clinical phenome and tissue genome.&nbsp;<br />\n\t</span></p>\n<div>\n\t&nbsp;</p>\n<div>\n\t<span>Please see the <span><a href="https://wiki.cancerimagingarchive.net/x/tgpp" target="_blank">TCGA-PRAD</a></span> wiki page to learn more about the images and to obtain any supporting metadata for this collection.</span></p>\n'
    assert collection['doi'] == '10.7937/K9/TCIA.2016.YXOGLM4Y'
    assert collection['image_types'] == 'CT, PT, MR, Pathology'
    assert collection['location'] == 'Prostate'
    assert collection['species'] == 'Human'
    assert collection['subject_count'] == 14
    assert collection['supporting_data'] == 'Clinical, Genomics'


def test_analysis_results(client, app):
    response = client.get('/v1/analysis_results')
    assert response.status_code == 200
    data = response.json['analysisResults']
    results = {r['description']: \
                   {key: r[key] for key in r.keys() if key != 'description'} \
                   for r in data}
    assert len(results) == NUM_ANALYSIS_RESULTS
    assert 'Standardized representation of the TCIA LIDC-IDRI annotations using DICOM' in results
    collection = results['Standardized representation of the TCIA LIDC-IDRI annotations using DICOM' ]
    # assert collection['idc_data_versions'] == ['1.0','2.0']
    assert collection['analysisArtifacts'] == 'Tumor segmentations, image features'
    assert collection['cancer_type'] == 'Lung'
    assert collection['collections'].lower().replace(' ','_').replace('-','_') =='lidc_idri'
    # assert collection['date_updated'] == '2016-08-29'
    assert collection['doi'] == '10.7937/TCIA.2018.h7umfurq'
    assert collection['location'] == 'Chest'
    assert collection['subject_count'] == 1010


def test_attributes(client, app):

    response = client.get('/v1/attributes')
    assert response.status_code == 200
    data = response.json
    data_sources = data["data_sources"]

    source_name = f'idc-dev-etl.idc_v{VERSIONS}.dicom_pivot_v{VERSIONS}'
    data_source = next(
        source for source in data_sources if source['data_source'] == source_name)
    attributes = {attribute['name']: {key: attribute[key] for key in attribute.keys() if key != 'name'} for attribute in data_source['attributes']}
    assert 'Modality' in attributes
    assert attributes['Modality'] == {'active': True, 'data_type': 'Categorical String', 'units': None}

    source_name = f'idc-dev-etl.idc_v*.tcga_biospecimen_rel9'
    data_source = next(
        source for source in data_sources if fnmatch(source['data_source'], source_name))
    attributes = {attribute['name']: {key: attribute[key] for key in attribute.keys() if key != 'name'} for attribute in data_source['attributes']}
    assert 'sample_type' in attributes
    # assert attributes['program_name']['dataSetTypes'][0]['data_type'] == 'Clinical, Biospecimen, and Mutation Data'
    assert attributes['sample_type'] == {'active': True, 'data_type': 'Categorical String', 'units': None}

    source_name = f'idc-dev-etl.idc_v*.tcga_clinical_rel9'
    data_source = next(
        source for source in data_sources if fnmatch(source['data_source'], source_name))
    attributes = {attribute['name']: {key: attribute[key] for key in attribute.keys() if key != 'name'} for attribute in data_source['attributes']}
    assert 'disease_code' in attributes
    # assert attributes['program_name']['dataSetTypes'][0]['data_type'] == 'Clinical, Biospecimen, and Mutation Data'
    assert attributes['disease_code'] == {'active': True, 'data_type': 'Categorical String', 'units': None}


