import json


# def test_user_cohorts(client, app):
#     response = client.get('v1/cohorts')

def test_create_cohort(client, app):
    # Create a filter set
    # collections = [{"program_name":"TCGA",
    #                 "collection_name":"BLCA",
    #                 "data_versions":[
    #                     {"attribute_group": 'TCGA Clinical and Biospecimen Data','version': 'r9'},
    #                     {'attribute_group': 'TCIA Image Data', 'version': '0'}]
    #                 }]
    filterSet = {
        "bioclin_version": "r9",
        "imaging_version": "0",
        "attributes": {
            "collection_id": ["TCGA-LUAD","TCGA-KIRC"],
            "Modality": ["CT", "MR"]}}

    cohortSpec = {"name":"testcohort",
                  "description":"Test description",
                  "filterSet":filterSet}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.post('/v1/cohorts', data=json.dumps(cohortSpec), headers=headers)
    assert response.content_type == 'application/json'

    assert response.status_code == 200
    cohortSpec = json.loads(response.json['cohortSpec'])
    assert cohortSpec['name']=="testcohort"
    assert cohortSpec['description']=="Test description"
    assert cohortSpec["filterSet"]["bioclin_version"]=="r9"
    assert "Modality" in cohortSpec["filterSet"]["attributes"]
    assert "TCGA-LUAD" in cohortSpec["filterSet"]["attributes"]["collection_id"]


# def test_cohort_preview(client, app):
#     # Create a filter set
#     collections = [{"program_name":"TCGA","collection_name":"BLCA","versions":["1.0"]}]
#     filter = {"program_name":["TCGA"], "project_short_name":["TCGA-LUAD","TCGA-KIRC"],"Modality":["CT","MR"]}
#     filterSet={"collections":collections,"filter":filter}
#
#     mimetype = ' application/json'
#     headers = {
#         'Content-Type': mimetype,
#         'Accept': mimetype
#     }
#     response = client.post('/v1/cohorts/preview',data=json.dumps(filterSet), headers=headers)
#     assert response.content_type == mimetype
#
#     assert response.status_code == 200
#     data = json.loads(response.json['programs'])
#     assert len(list(filter(lambda program: program['short_name'] == "TCGA", data))) == 1
#     assert len(list(filter(lambda program: program['name'] == "The Cancer Genome Atlas", data))) == 1
