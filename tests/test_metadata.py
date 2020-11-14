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


def test_versions(client, app):
    response = client.get('/v1/versions')
    assert response.status_code == 200
    data = response.json['versions']
    versions = {version['idc_data_version']: {key: version[key] for key in version.keys() if key != 'version_number'} for version in data}
    assert len(versions) == 1
    assert "1.0" in versions
    assert versions["1.0"]["active"] == True
    # assert versions["1.0"]['name'] == 'Imaging Data Commons Data Release'
    assert versions["1.0"]["data_sources"] == \
           [{'data_type': 'Clinical, Biospecimen, and Mutation Data',
             'name': 'isb-cgc.TCGA_bioclin_v0.Biospecimen'},
            {'data_type': 'Clinical, Biospecimen, and Mutation Data',
             'name': 'isb-cgc.TCGA_bioclin_v0.clinical_v1'},
            {'data_type': 'Image Data', 'name': 'idc-dev.metadata.dicom_pivot_wave1'}]
    programs = {program['short_name']: {key: program[key] for key in program.keys() if key != 'short_name'} for program in versions["1.0"]["programs"]}
    assert "TCGA" in programs
    assert programs["TCGA"]["name"] == "The Cancer Genome Atlas"
    assert "ISPY" in programs
    assert "LIDC" in programs
    assert "QIN" in programs
    assert "NSCLCR" in programs
    assert len(programs) == 5


def test_collections(client, app):

    query_string = dict(
        program_name = "TCGA",
        idc_data_version = "1.0"
    )

    response = client.get('/v1/collections',
                          query_string = query_string)
    assert response.status_code == 200
    data = response.json['programs']
    programs = {program['program_name']: {key: program[key] for key in program.keys() if key != "program_name"} for program in data}
    collections = {collection['collection_id']: {key: collection[key] for key in collection.keys() if key != 'collection_id'} for collection in programs['TCGA']['collections']}
    assert len(collections) == 21
    assert "tcga_prad" in collections
    assert collections['tcga_prad'] == \
           {'idc_data_versions': ['1.0'], 'active': True, 'cancer_type': 'Prostate Cancer',
            'collection_type': 'Original', 'date_updated': '2016-08-29',
            'description': '<div>\n\t<strong>Note:&nbsp;This collection has special restrictions on its usage. See <a href="https://wiki.cancerimagingarchive.net/x/c4hF" target="_blank">Data Usage Policies and Restrictions</a>.</strong></p>\n<div>\n\t&nbsp;</p>\n<div>\n\t<span>The <a href="http://imaging.cancer.gov/" target="_blank"><u>Cancer Imaging Program (CIP)</u></a></span><span>&thinsp;</span><span> is working directly with primary investigators from institutes participating in TCGA to obtain and load images relating to the genomic, clinical, and pathological data being stored within the <a href="http://tcga-data.nci.nih.gov/" target="_blank">TCGA Data Portal</a>.&nbsp;Currently this image collection of prostate adenocarcinoma (PRAD) patients can be matched by each unique case identifier with the extensive gene and expression data of the same case from The Cancer Genome Atlas Data Portal to research the link between clinical phenome and tissue genome.&nbsp;<br />\n\t</span></p>\n<div>\n\t&nbsp;</p>\n<div>\n\t<span>Please see the <span><a href="https://wiki.cancerimagingarchive.net/x/tgpp" target="_blank">TCGA-PRAD</a></span> wiki page to learn more about the images and to obtain any supporting metadata for this collection.</span></p>\n',
            'doi': '10.7937/K9/TCIA.2016.YXOGLM4Y', 'image_types': 'CT, PT, MR, Pathology', 'location': 'Prostate',
            'owner_id': 1, 'species': 'Human', 'subject_count': 14, 'supporting_data': 'Clinical Genomics'}


    query_string = dict(
        program_name = "",
        idc_data_version = "1.0"
    )

    response = client.get('/v1/collections',
                          query_string = query_string)
    assert response.status_code == 200
    data = response.json['programs']
    programs = {program['program_name']: {key: program[key] for key in program.keys() if key != "program_name"} for program in data}
    collections = {collection['collection_id']: {key: collection[key] for key in collection.keys() if key != 'collection_id'} for collection in programs['TCGA']['collections']}
    assert len(collections) == 21
    assert "tcga_prad" in collections
    assert collections['tcga_prad'] == \
           {'idc_data_versions': ['1.0'], 'active': True, 'cancer_type': 'Prostate Cancer',
            'collection_type': 'Original', 'date_updated': '2016-08-29',
            'description': '<div>\n\t<strong>Note:&nbsp;This collection has special restrictions on its usage. See <a href="https://wiki.cancerimagingarchive.net/x/c4hF" target="_blank">Data Usage Policies and Restrictions</a>.</strong></p>\n<div>\n\t&nbsp;</p>\n<div>\n\t<span>The <a href="http://imaging.cancer.gov/" target="_blank"><u>Cancer Imaging Program (CIP)</u></a></span><span>&thinsp;</span><span> is working directly with primary investigators from institutes participating in TCGA to obtain and load images relating to the genomic, clinical, and pathological data being stored within the <a href="http://tcga-data.nci.nih.gov/" target="_blank">TCGA Data Portal</a>.&nbsp;Currently this image collection of prostate adenocarcinoma (PRAD) patients can be matched by each unique case identifier with the extensive gene and expression data of the same case from The Cancer Genome Atlas Data Portal to research the link between clinical phenome and tissue genome.&nbsp;<br />\n\t</span></p>\n<div>\n\t&nbsp;</p>\n<div>\n\t<span>Please see the <span><a href="https://wiki.cancerimagingarchive.net/x/tgpp" target="_blank">TCGA-PRAD</a></span> wiki page to learn more about the images and to obtain any supporting metadata for this collection.</span></p>\n',
            'doi': '10.7937/K9/TCIA.2016.YXOGLM4Y', 'image_types': 'CT, PT, MR, Pathology', 'location': 'Prostate',
            'owner_id': 1, 'species': 'Human', 'subject_count': 14, 'supporting_data': 'Clinical Genomics'}

    collections = {collection['collection_id']: {key: collection[key] for key in collection.keys() if key != 'collection_id'} for collection in programs['ISPY']['collections']}

    assert 'ispy1' in collections
    assert len(collections) == 1
    assert collections['ispy1'] == \
           {'active': True, 'cancer_type': 'Breast Cancer', 'collection_type': 'Original',
            'date_updated': '2016-08-31',
            'description': '<p>\n\tISPY1/ACRIN 6657 was designed as a prospective study to test MRI for ability to predict response to treatment and risk-of-recurrence in patients with stage 2 or 3 breast cancer receiving neoadjuvant chemotherapy (NACT). ACRIN 6657 was conducted as a companion study to CALGB 150007, a correlative science study evaluating tissue-based biomarkers in the setting of neoadjuvant treatment of breast cancer. Collectively, CALGB 150007 and ACRIN 6657 formed the basis of the multicenter Investigation of Serial Studies to Predict Your Therapeutic Response with Imaging and moLecular Analysis (I-SPY TRIAL) breast cancer trial, a study of imaging and tissue-based biomarkers for predicting pathologic complete response (pCR) and recurrence-free survival (RFS).<br />\n\t<br />\n\tThe collection consists of 847 MR studies from 222 subjects.<br />\n\t<br />\n\tPlease see the <a href="https://wiki.cancerimagingarchive.net/display/Public/ISPY1">ISPY1</a> wiki pageto learn more about the images and to obtain any supporting metadata for this collection.</p>\n',
            'doi': '10.7937/K9/TCIA.2016.HdHpgJLK', 'idc_data_versions': ['1.0'], 'image_types': 'MR, SEG',
            'location': 'Breast', 'owner_id': 1, 'species': 'Human', 'subject_count': 222,
            'supporting_data': 'Clinical, Image Analyses'}


def test_attributes(client, app):
    query_string = dict(
        idc_data_version = '',
        data_source = 'idc-dev.metadata.dicom_pivot_wave1'
    )
    response = client.get('/v1/attributes',
                          query_string = query_string)
    assert response.status_code == 200
    data = response.json['data_sources']
    data_sources = {data_source['data_source']: {key: data_source[key] for key in data_source.keys() if key != 'data_source'} for data_source in data}
    attributes = {attribute['name']: {key: attribute[key] for key in attribute.keys() if key != 'name'} for attribute in data_sources[query_string['data_source']]['attributes']}
    assert 'Modality' in attributes
    assert attributes['Modality'] == {'active': True, 'data_type': 'Categorical String', 'idc_data_version': '1.0', 'units': None}

    query_string = dict(
        idc_data_version='',
        data_source = 'isb-cgc.TCGA_bioclin_v0.Biospecimen'
    )
    response = client.get('/v1/attributes',
                          query_string = query_string)
    assert response.status_code == 200
    data = response.json['data_sources']
    data_sources = {data_source['data_source']: {key: data_source[key] for key in data_source.keys() if key != 'data_source'} for data_source in data}
    attributes = {attribute['name']: {key: attribute[key] for key in attribute.keys() if key != 'name'} for attribute in data_sources[query_string['data_source']]['attributes']}
    assert 'program_name' in attributes
    # assert attributes['program_name']['dataSetTypes'][0]['data_type'] == 'Clinical, Biospecimen, and Mutation Data'
    assert attributes['program_name'] == {'active': True, 'data_type': 'Categorical String', 'idc_data_version': '1.0', 'units': None}

    query_string = dict(
        idc_data_version='',
    data_source = 'isb-cgc.TCGA_bioclin_v0.clinical_v1'
    )
    response = client.get('/v1/attributes',
                          query_string = query_string)
    assert response.status_code == 200
    data = response.json['data_sources']
    data_sources = {data_source['data_source']: {key: data_source[key] for key in data_source.keys() if key != 'data_source'} for data_source in data}
    attributes = {attribute['name']: {key: attribute[key] for key in attribute.keys() if key != 'name'} for attribute in data_sources[query_string['data_source']]['attributes']}
    assert 'program_name' in attributes
    # assert attributes['program_name']['dataSetTypes'][0]['data_type'] == 'Clinical, Biospecimen, and Mutation Data'
    assert attributes['program_name'] == {'active': True, 'data_type': 'Categorical String', 'idc_data_version': '1.0', 'units': None}



def test_attributes_all_data_sources(client, app):
    query_string = dict(
        idc_data_version = '',
        data_source = ''
    )
    response = client.get('/v1/attributes',
                          query_string = query_string)
    assert response.status_code == 200
    data = response.json['data_sources']
    data_sources = {data_source['data_source']: {key: data_source[key] for key in data_source.keys() if key != 'data_source'} for data_source in data}
    for data_source in data_sources:
        attributes = {attribute['name']: {key: attribute[key] for key in attribute.keys() if key != 'name'} for attribute in data_sources[data_source]['attributes']}
        if data_source == 'idc-dev.metadata.dicom_pivot_wave1':
            assert 'Modality' in attributes
            assert attributes['Modality'] == {'active': True, 'data_type': 'Categorical String', 'idc_data_version': '1.0', 'units': None}
        elif data_source == 'isb-cgc.TCGA_bioclin_v0.Biospecimen':
            assert 'program_name' in attributes
            # assert attributes['program_name']['dataSetTypes'][0]['data_type'] == 'Clinical, Biospecimen, and Mutation Data'
            assert attributes['program_name'] == {'active': True, 'data_type': 'Categorical String',
                                                  'idc_data_version': '1.0', 'units': None}
        elif data_source == 'isb-cgc.TCGA_bioclin_v0.clinical_v1':
            assert 'program_name' in attributes
            # assert attributes['program_name']['dataSetTypes'][0]['data_type'] == 'Clinical, Biospecimen, and Mutation Data'
            assert attributes['program_name'] == {'active': True, 'data_type': 'Categorical String', 'idc_data_version': '1.0', 'units': None}
        elif data_source == 'idc-dev.metadata.dicom_pivot_wave1':
            assert 'Modality' in attributes
            assert attributes['Modality'] == {'active': True, 'data_type': 'Categorical String', 'idc_data_version': '1.0', 'units': None}
        else:
            assert 0==1


