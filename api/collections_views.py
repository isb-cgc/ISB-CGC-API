#
# Copyright 2019, Institute for Systems Biology
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

import logging
import django

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

#  from idc_collections.models import Collection, CollectionVersion, CollectionField, FieldEnumerant

logger = logging.getLogger(settings.LOGGER_NAME)


# def get_collections():
#     DJANGO_URI = os.getenv('DJANGO_URI')
#     try:
#         result = requests.get("{}/{}".format(DJANGO_URI, 'collections/'))
#     except:
#         if result.status_code != 200:
#            raise Exception("oops!")
#     #response = result.json()
#     return result
#
#     django.setup()
#     collections = None
#     try:
#         collections = [
#             {
#                 'name': collection.name,
#                 'description': collection.description,
#                 'versions': [{'version': version.version, 'date': version.date} for version in CollectionVersion.objects.filter(collection=collection)]
#             }
#             for collection in Collection.objects.all()
#         ]
#     except Exception as e:
#         logger.exception(e)
#
#     return collections
#
# def get_collection_info(collection_id, version):
#     django.setup()
#     collection_info = None
#     try:
#         #collectionVersion = CollectionVersion.objects.get(collection=collection_id, version=version)
#         #collectionFields = CollectionField.objects.filter(collectionVersions=collectionVersion)
#         collectionFields = CollectionField.objects.filter(
#             collectionVersion__collection=collection_id,
#             collectionVersion__version=version)
#         collection_info = [
#             field.field_name for field in collectionFields
#         ]
#     except ObjectDoesNotExist as e:
#         logger.warning("Collection {}, version {} was not found!".format(str(collection_id), str(version)))
#     except Exception as e:
#         logger.exception(e)
#
#     return collection_info
#
# def get_collection_field_info(collection_id, version, field_name):
#     django.setup()
#     field_info = None
#     try:
#         #collectionVersion = CollectionVersion.objects.filter(collection=collection_id, version=version)
#         #field = CollectionField.objects.filter(versions=collectionVersion, field_name=field_name)
#         field = CollectionField.objects.filter(
#             collectionVersion__collection=collection_id,
#             collectionVersion__version=version,
#             field_name=field_name)
#         field_info = {
#             "fieldname": field.field_name,
#             "description": field.description,
#             "fieldType": field.field_type[0],
#             "enumerated_values": [
#                 enumeratedValue.enumerant for enumeratedValue in FieldEnumerant.objects.filter(field=field_name)
#             ]
#         }
#     except ObjectDoesNotExist as e:
#         logger.warning("Field {}, in Collection {}, version {} was not found!".format(str(field_name), str(collection_id), str(version)))
#     except Exception as e:
#         logger.exception(e)
#
#     return field_info
