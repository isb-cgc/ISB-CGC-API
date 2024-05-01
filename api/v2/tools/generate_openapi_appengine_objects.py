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

# Generate the 'filters' and fields definitions to be inserted in openapi-appengine.yaml.
# Ideally, these could stay in a separate yaml file which openapi-appengine.yaml would reference,
# but such external references are not support by Google appengine.
# Therefore the schemas must be manually inserted into openapi-appengine.yaml.
# This script should be run whenever the set of filters and fields change. This at least
# means when dicom_pivot_vX changes.
# The script queries the IDC API on localhost, and the webapp must be running on Vagrant
# when the script is executed.
import requests
import sys
import argparse
from google.cloud import bigquery

integer_continuous_numerics = (
    'age_at_diagnosis',
    'max_TotalPixelMatrixColumns',
    'max_TotalPixelMatrixRows',
    'min_PixelSpacing'
)

def get_filter_metadata(args):
    url = 'http://localhost:8095/v2/filters'
    headers = {'accept': 'application/json'}
    response = requests.get(url)
    response = response.json()
    return response

def get_field_metadata(args):
    url = 'http://localhost:8095/v2/fields/current'
    headers = {'accept': 'application/json'}
    response = requests.get(url).json()
    return response


def write_required_fields(f):
    f.write(
"""
swagger: "2.0"
info:
  description: "IDC API Endpoints, version 1"
  title: "IDC API"
  version: "1.0"
paths:
definitions:
"""
    )
    return

# Perform a query and write results to dst_dataset.dst_table
def query_BQ(client, dst_dataset, dst_table, sql, write_disposition='WRITE_APPEND',
             schema_update_options = None, expiration=0):


    table_id = "{}.{}.{}".format(client.project, dst_dataset, dst_table)
    job_config = bigquery.QueryJobConfig(destination=table_id)
    job_config.write_disposition = write_disposition
    job_config.schema_update_options = schema_update_options

    try:
        job = client.query(sql, job_config=job_config)
    except Exception as exc:
        print("Error loading table: {},{},{}".format(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]),
              file=sys.stdout, flush=True)
        raise

    result = job.result()
    return result

def get_accepted_values(client, source, filter):
    if filter['accepted_values']:
        accepted_values = sorted(list(filter['accepted_values'].values()))
    else:
        query = f"""
        SELECT DISTINCT {filter['name']}
        FROM `{source}`
        ORDER BY {filter['name']}
        """
        try:
            accepted_values = [row[filter['name']] for row in client.query(query)]
        except Exception as exc:
            print(f'Exception: {exc}')
            accepted_values = []

    return accepted_values


def write_filter(client, f, source, filter):
    name = filter['name']
    data_type = {
        # 'Continuous Numeric': 'number',
        'Ranged Number': 'number',
        'Ranged Integer': 'integer',
        'Categorical Number': 'number',
        'Integer': 'integer',
        'Categorical String':'string',
        'String': 'string'
    }[filter['data_type']]
    # integer_continuous_numerics = (
    #     'age_at_diagnosis',
    #     'max_TotalPixelMatrixColumns',
    #     'max_TotalPixelMatrixRows',
    #     'min_PixelSpacing'
    # )

    f.write('      {}:'.format(name))
    f.write(
"""
        type: "array"
        items:
          type:"""
    )
    if filter['data_type'].startswith('Ranged'):
        # Some continuous numerics aren't really continuous
        if name.startswith(integer_continuous_numerics):
            data_type = 'integer'

        f.write(f' "{data_type}"\n')
        items = 2 if name.split('_')[-1] in ['ebtwe', 'ebtw', 'btwe', 'btw'] else 1
        f.write(f'        minItems: {items}\n')
        f.write(f'        maxItems: {items}\n')
    else:
        f.write(f' "{data_type}"\n')
        f.write('        minItems: 1\n')

    return


def gen_filters_schema(args, filters):
    client = bigquery.Client('idc-dev-etl')

    with open(args.filters_file, "w") as f:
        write_required_fields(f)
        f.write(
"""  filters:
    type: "object"
    properties:
"""
        )
        names = []
        all_filters = [filter for source in filters['data_sources'] for filter in source['filters']]
        for source in filters['data_sources']:
            for filter in source ['filters']:
                if not filter['name'] in names:
                    write_filter(client, f, source['data_source'], filter)
                    names.append(filter['name'])
        f.write('    additionalProperties: False\n')
    return


def gen_fields_schema(args, fields):
    all_fields = set()
    for source in fields['data_sources']:
        all_fields  = all_fields.union(source['fields'])

    with open(args.query_file, "w") as f:
        write_required_fields(f)
        f.write(
"""  fields:
    type: "object"
    properties:
      fields:
        type: "array"
        items:
          type: "string"
          enum: [
"""
        )
        for field in sorted(list(all_fields), key=str.lower):
            f.write(f'            "{field}",\n')
        f.write(
            """      ]
            """
        )

    return


# def gen_manifest_data(args, fields, filters):
#     pivot_filters = next(source for source in filters['data_sources'] if 'pivot' in source['data_source'])
#     client = bigquery.Client('idc-dev-etl')
#     dicom_pivot = client.get_table('idc-dev-etl.idc_current.dicom_pivot')
#     schema = {row.name: row for row in dicom_pivot.schema}
#     schema = {}
#     for source in filters['data_sources']:
#         table = client.get_table(source['data_source'])
#         t = {row.name: row for row in table.schema}
#         schema.update(t)
#
#     all_fields = set()
#     for source in fields['data_sources']:
#         all_fields  = all_fields.union(source['fields'])
#
#     with open(args.query_result_file, "w") as f:
#         write_required_fields(f)
#         f.write(
# """  manifestData:
#     type: "array"
#     items:
#       type: "object"
#       properties:
# """
#         )
#         for field in sorted(list(all_fields), key=str.lower):
#             if field in schema:
#                 data_type = {'STRING': 'string',
#                              'FLOAT': 'number',
#                              'DATE': 'string',
#                              'INTEGER': 'integer',
#                              'NUMERIC': 'number'}[schema[field].field_type]
#
#             else:
#                 try:
#                     data_type = {
#                         'CancerType': 'string',
#                         'gcs_generation': 'string',
#                     }[field]
#                 except Exception as exc:
#                     if field in ['counts', 'group_size']:
#                         continue
#                     print(f'Unknown data type for field {field}; {exc}')
#
#             f.write(f'        {field}:\n')
#             f.write(f'          type:  "{data_type}"\n')
#         for field in [
#             'instance_count',
#             'series_count',
#             'study_count',
#             'patient_count',
#             'collection_count',
#             'group_size',
#         ]:
#             f.write(f'        {field}:\n')
#             f.write(f'          type:  "number"\n')
#
#
#     return


def gen_json(args):
    filters = get_filter_metadata(args)
    gen_filters_schema(args, filters)

    fields = get_field_metadata(args)
    gen_fields_schema(args, fields)

    # gen_manifest_data(args, fields, filters)
    # # # gen_query_results_schema(args, filters)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filters_file', default='filters.yaml',
                        help='File into which to save the generated yaml')
    parser.add_argument('--query_file', default='fields.yaml',
                        help='File into which to save the generated fields yaml')
    # parser.add_argument('--query_result_file', default='manifest_data.yaml',
    #                     help='File into which to save the generated manifest data yaml')
    args = parser.parse_args()
    print("{}".format(args), file=sys.stdout)
    gen_json(args)
