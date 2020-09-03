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

def gen_json(args):
    attributes = get_attributes_from_webapp()

    with open(args.filters_file, "w") as f:
        f.write(
"""
  filters:
    type: "object"
    properties:
"""
        )
        for attribute in attributes:
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
            elif data_type ==  'Categorical String':
                f.write(' "string"\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filters_file', default='../filters_schema.yaml',
                        help='File into which to save the generated yaml schema')
    args = parser.parse_args()
    print("{}".format(args), file=sys.stdout)
    gen_json(args)
