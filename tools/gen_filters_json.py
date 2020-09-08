import requests
import sys
import argparse
import json

# Generate the 'filters' schema to be inserted in openapi-appengine.yaml.
# Ideally, this could stay in a separate yaml file which openapi-appengine.yaml references,
# but can't get that to work, so must be manually inserted when the attributes change.

def get_attributes_from_webapp():
    response = requests.get('http://127.0.0.1:8085/collections/api/attributes/')
    attributes = response.json()['attributes']
    return attributes

def write_continuous_numeric(f, attribute):
    for suffix in ['_lt', '_lte', '_btw', '_gte', '_gt']:
        f.write('      {}{}:'.format(attribute['name'],suffix))
        f.write(
"""
        type: "array"
        items:
          type:"""
        )
        f.write(' "number"\n')


def write_attribute(f, attribute):
    f.write('      {}:'.format(attribute['name']))
    f.write(
"""
        type: "array"
        items:
          type:"""
    )
    data_type = attribute['data_type']
    if data_type in ['Text', 'String']:
        f.write(' "string"\n')
    elif data_type == 'Integer':
        f.write(' "integer"\n')
    elif data_type == 'Continuous Numeric':
        f.write(' "number"\n')
        # write_continuous_numeric(f, attribute)
    elif data_type == 'Categorical String':
        f.write(' "string"\n')


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
    attributes = get_attributes_from_webapp()

    gen_filters_schema(args, attributes)
    gen_query_schema(args, attributes)
    gen_query_results_schema(args, attributes)

    with open(args.filters_file, "w") as f:
        f.write(
"""  filters:
    type: "object"
    properties:
"""
        )
        for attribute in attributes:
            write_attribute(f, attribute)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filters_file', default='../filters_schema.yaml',
                        help='File into which to save the generated yaml schema')
    parser.add_argument('--query_file', default='../query_schema.yaml',
                        help='File into which to save the generated queryFields schema')
    parser.add_argument('--query_results_file', default='../query_results_schema.yaml',
                        help='File into which to save the generated queryResults schema')
    args = parser.parse_args()
    print("{}".format(args), file=sys.stdout)
    gen_json(args)
