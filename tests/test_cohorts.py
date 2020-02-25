import json

# Utility to create a "standard" cohort for testing
def create_cohort(client):
    # Create a filter set
    filterSet = {
        "bioclin_version": "r9",
        "imaging_version": "0",
        "attributes": {
            "collection_id": ["TCGA-LUAD", "TCGA-KIRC"],
            "Modality": ["CT", "MR"],
            "Race": ["WHITE"]}}

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filterSet": filterSet}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.post('/v1/cohorts', data=json.dumps(cohortSpec), headers=headers)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohortResponse = json.loads(response.json['cohortSpec'])

    return cohortResponse



def test_create_cohort(client, app):
    # Create a filter set
    filterSet = {
        "bioclin_version": "r9",
        "imaging_version": "0",
        "attributes": {
            "collection_id": ["TCGA-LUAD", "TCGA-KIRC"],
            "Modality": ["CT", "MR"],
            "Race": ["WHITE"]}}

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
    cohortResponse = json.loads(response.json['cohortSpec'])

    assert cohortResponse['name']=="testcohort"
    assert cohortResponse['description']=="Test description"
    assert cohortResponse["filterSet"]["bioclin_version"]=="r9"
    assert "Modality" in cohortResponse["filterSet"]["attributes"]
    assert "TCGA-LUAD" in cohortResponse["filterSet"]["attributes"]["collection_id"]

    # # Delete the cohort we just created
    # response = client.get("{}/{}/".format('v1/cohorts/delete', cohortResponse['id']))
    # assert response.content_type == 'application/json'
    # assert response.status_code == 200


def test_get_cohort(client, app):

    # Create a cohort to test against
    attributes = {
        "collection_id": ["TCGA-READ"],
        "Modality": ["CT", "MR"],
        "race": ["WHITE"]}
    filterSet = {
        "bioclin_version": "r9",
        "imaging_version": "0",
        "attributes": attributes}

    cohortSpec = {"name": "testcohort",
                  "description": "Test description",
                  "filterSet": filterSet}

    mimetype = ' application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.post('/v1/cohorts', data=json.dumps(cohortSpec), headers=headers)
    assert response.status_code == 200
    cohortResponse = json.loads(response.json['cohortSpec'])

    query_string = {
        'return_level': 'Instance',
        # 'fetch_count': 5
    }

    # Get the list of objects in the cohort
    response = client.get("{}/{}/".format('v1/cohorts', cohortResponse['id']),
                query_string = query_string)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohort = json.loads(response.json['cohort'])

    assert cohort['name']=="testcohort"
    assert cohort['description']=="Test description"
    assert cohort['filterSet'] == filterSet
    assert len(cohort['collections']) == 1
    assert cohort['collections'][0]['collection_id'].lower() == 'TCGA-READ'.lower()
    assert len(cohort['collections'][0]['patients']) == 2
    # assert cohort['collections'][0]['patients'][0]['patientID'].lower() == 'TCGA-CL-5917'.lower()
    # assert len(cohort['collections'][0]['patients'][1]['studies']) == 2
    # assert len(cohort['collections'][0]['patients'][1]['studies'][0]['series']) == 27
    # assert len(cohort['collections'][0]['patients'][1]['studies'][0]['series'][0]['instances']) == 54

def test_list_cohorts(client,app):
    cohort1 = create_cohort(client)['id']
    cohort2 = create_cohort(client)['id']

    # Get the list of cohorts
    response = client.get("{}/".format('v1/cohorts'))
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    cohorts = json.loads(response.json['cohortList'])
    assert len(list(filter(lambda cohort: cohort['id'] == cohort1, cohorts))) == 1
    assert len(list(filter(lambda cohort: cohort['id'] == cohort2, cohorts))) == 1


# def test_delete_cohorts(client, app):
#     # Create a filter set
#     filterSet = {
#         "bioclin_version": "r9",
#         "imaging_version": "0",
#         "attributes": {
#             "collection_id": ["TCGA-LUAD", "TCGA-KIRC"],
#             "Modality": ["CT", "MR"],
#             "Race": ["WHITE"]}}
#
#     cohortSpec = {"name": "testcohort",
#                   "description": "Test description",
#                   "filterSet": filterSet}
#
#     mimetype = ' application/json'
#     headers = {
#         'Content-Type': mimetype,
#         'Accept': mimetype
#     }
#     response = client.post('/v1/cohorts', data=json.dumps(cohortSpec), headers=headers)
#     assert response.content_type == 'application/json'
#     assert response.status_code == 200
#     cohortResponse = json.loads(response.json['cohortSpec'])
#
#     # Delete the cohort we just created
#     response = client.get("{}/{}/".format('v1/cohorts/delete', cohortResponse['id']))
#     assert response.content_type == 'application/json'
#     assert response.status_code == 200




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
