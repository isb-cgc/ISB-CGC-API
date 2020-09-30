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

import requests
import sys
import argparse
import json
import os
from os.path import join, dirname
from google.cloud import storage
import subprocess
import ast

# Generate the 'filters' schema to be inserted in openapi-appengine.yaml.
# Ideally, this could stay in a separate yaml file which openapi-appengine.yaml references,
# but can't get that to work, so must be manually inserted when the attributes change.

def get_db_metadata(args):
    subprocess.run(['gsutil', 'cp', args.collex_metadata_blob, args.collex_metadata_file])
    with open(args.collex_metadata_file) as f:
        attrib_string = f.read().split("INSERT INTO `idc_collections_attribute` VALUES ")[1].split(';')[0]
        attribs = list(ast.literal_eval(attrib_string.replace('NULL,','')))

    return attribs


def write_continuous_numeric(f, name, min_max):
    f.write('      {}:'.format(name))
    f.write(
"""
        type: "array"
        items:
          type:"""
        )
    f.write(' "number"\n')
    f.write('        minItems: {}\n'.format(min_max))
    f.write('        maxItems: {}\n'.format(min_max))


def write_attribute(f, attribute):
    name = attribute[1]
    f.write('      {}:'.format(name))
    f.write(
"""
        type: "array"
        items:
          type:"""
    )
    data_type = attribute[3]
    if data_type in ['T', 'S', 'C']:
        f.write(' "string"\n')
        f.write('        minItems: 1\n')
    elif data_type == 'M':
        f.write(' "integer"\n')
        f.write('        minItems: 1\n')
    elif data_type == 'N':
        f.write(' "number"\n')
        f.write('        minItems: 1\n')
        f.write('        maxItems: 1\n')
        for details in [('_lt',1), ('_lte',1), ('_btw',2), ('_gte',1), ('_gt',1)]:
            write_continuous_numeric(f,"{}{}".format(name,details[0]),details[1])

    # data_type = attribute['data_type']
    # if data_type in ['Text', 'String']:
    #     f.write(' "string"\n')
    # elif data_type == 'Integer':
    #     f.write(' "integer"\n')
    # elif data_type == 'Continuous Numeric':
    #     f.write(' "number"\n')
    #     # write_continuous_numeric(f, attribute)
    # elif data_type == 'Categorical String':
    #     f.write(' "string"\n')


def gen_filters_schema(args, attributes):
    with open(args.filters_file, "w") as f:
        f.write(
"""  filters:
    type: "object"
    properties:
"""
        )
        for attribute in attributes:
            write_attribute(f, attribute)
        f.write('    additionalProperties: False\n')

def gen_query_schema(args, attributes):
    with open(args.query_file, "w") as f:
        f.write(
"""  queryFields:
    type: "array"
    items:
      type: "string"
      enum: [
"""
        )
        for attribute in attributes:
            if 'Image Data' in attribute['dataSetTypes'] or 'Derived Data' in attribute['dataSetTypes']:
                if not attribute['name'].endswith(('_lt', '_lte', '_btw', '_gte', '_gt')):
                        f.write('        "{}",\n'.format(attribute['name'].rsplit('_', 1)[0]))
        f.write(
"""      ]
"""
        )

def gen_query_schema(args, attributes):
    with open(args.query_file, "w") as f:
        f.write(
"""  queryFields:
    type: "array"
    items:
      type: "string"
      enum: [
"""
        )
        for attribute in attributes:
            if 'Image Data' in attribute['dataSetTypes'] or 'Derived Data' in attribute['dataSetTypes']:
                if not attribute['name'].endswith(('_lt', '_lte', '_btw', '_gte', '_gt')):
                        f.write('        "{}",\n'.format(attribute['name'].rsplit('_', 1)[0]))
        f.write(
"""      ]
"""
        )

def gen_query_results_schema(args, attributes):
    with open(args.query_results_file, "w") as f:
        f.write(
"""  queryResults:
    type: "object"
    properties:
"""
        )
        for attribute in attributes:
            if 'Image Data' in attribute['dataSetTypes'] or 'Derived Data' in attribute['dataSetTypes']:
                if not attribute['name'].endswith(('_lt', '_lte', '_btw', '_gte', '_gt')):
                    write_attribute(f, attribute)


def gen_json(args):
    attributes = get_db_metadata(args)

    gen_filters_schema(args, attributes)

    # Mpt yet supporting /query
    # gen_query_schema(args, attributes)
    # gen_query_results_schema(args, attributes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--collex_metadata_blob', default = "gs://idc-dev-files/idc_dev_collex_metadata.sql")
    parser.add_argument('--collex_metadata_file', default = "idc_dev_collex_metadata.sql")
    parser.add_argument('--filters_file', default='filters_schema.yaml',
                        help='File into which to save the generated yaml schema')
    parser.add_argument('--query_file', default='query_schema.yaml',
                        help='File into which to save the generated queryFields schema')
    parser.add_argument('--query_results_file', default='query_results_schema.yaml',
                        help='File into which to save the generated queryResults schema')
    args = parser.parse_args()
    print("{}".format(args), file=sys.stdout)
    gen_json(args)
