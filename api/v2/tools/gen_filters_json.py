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

# Generate the 'filters' and queryFields schemas to be inserted in openapi-appengine.yaml.
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


def get_db_metadata(args):
    url = 'http://localhost:8095/v2/filters'
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


def write_filter(f, filter):
    name = filter['name']
    data_type = {
        'Continuous Numeric': 'number',
        'Categorical Number': 'number',
        'Integer': 'integer',
        'Categorical String':'string',
        'String': 'string'
    }[filter['data_type']]

    f.write('      {}:'.format(name))
    f.write(
"""
        type: "array"
        items:
          type:"""
    )
    if data_type == 'number':
        f.write(f' "{data_type}"\n')
        items = 2 if name.split('_')[-1] in ['ebtwe', 'ebtw', 'btwe', 'btw'] else 1
        f.write(f'        minItems: {items}\n')
        f.write(f'        maxItems: {items}\n')
    else:
        f.write(f' "{data_type}"\n')
        f.write('        minItems: 1\n')

    return


def gen_filters_schema(args, filters):

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
                    write_filter(f, filter)
                    names.append(filter['name'])
        f.write('    additionalProperties: False\n')
    return


def gen_query_schema(args, filters):
    with open(args.query_file, "w") as f:
        write_required_fields(f)
        f.write(
# """
#   queryFields:
#     type: "array"
#     items:
#       type: "string"
#       enum: [
# """

"""
  queryFields:
    type: "object"
    properties:
      fields:
        type: "array"
        items:
          type: "string"
          enum: [
"""
        )

        source = next(source for source in filters['data_sources'] if source['data_source'].find('dicom_pivot') != -1)
        for filter in source['filters']:
            if filter['data_type'] != 'Continuous Numeric' or \
                    filter['name'].split('_')[-1] not in ('lt', 'lte', 'btw', 'ebtw', 'ebtwe', 'btwe', 'gte', 'gt'):
                name = filter['name']
                f.write(f'        "{name}",\n')
        # Add two additonal query fields
        f.write(f'        "counts",\n')
        f.write(f'        "sizes",\n')
        f.write(
"""      ]
"""
        )

    return


def gen_json(args):
    filters = get_db_metadata(args)

    gen_filters_schema(args, filters)

    gen_query_schema(args, filters)
    # gen_query_results_schema(args, filters)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filters_file', default='filters.yaml',
                        help='File into which to save the generated yaml schema')
    parser.add_argument('--query_file', default='queryfields.yaml',
                        help='File into which to save the generated queryFields schema')
    # parser.add_argument('--query_results_file', default='query_results_schema.yaml',
    #                     help='File into which to save the generated queryResults schema')
    args = parser.parse_args()
    print("{}".format(args), file=sys.stdout)
    gen_json(args)
