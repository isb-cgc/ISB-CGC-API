"""

Copyright 2015, Institute for Systems Biology

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import endpoints
import logging
import MySQLdb

from django.core.signals import request_finished
from protorpc import remote, messages

from isb_cgc_api_helpers import ISB_CGC_Endpoints, build_constructor_dict_for_message
from message_classes import MetadataAnnotationItem
from api.api_helpers import sql_connection

logger = logging.getLogger(__name__)


class MetadataAnnotationList(messages.Message):
    items = messages.MessageField(MetadataAnnotationItem, 1, repeated=True)
    count = messages.IntegerField(2, variant=messages.Variant.INT32)


class SamplesAnnotationsQueryBuilder(object):

    def build_query(self):
        query_str = 'select * ' \
                    'from metadata_annotation ' \
                    'where SampleBarcode=%s'

        return query_str


@ISB_CGC_Endpoints.api_class(resource_name='samples')
class SamplesAnnotationAPI(remote.Service):

    GET_RESOURCE = endpoints.ResourceContainer(sample_barcode=messages.StringField(1, required=True))

    @endpoints.method(GET_RESOURCE, MetadataAnnotationList,
                      path='samples/{sample_barcode}/annotations', http_method='GET')
    def annotations(self, request):
        """
        Returns TCGA annotations about a specific sample,
        Takes a patient barcode (of length , *eg* TCGA-01-0628-11A) as a required parameter.
        User does not need to be authenticated.
        """

        cursor = None
        db = None

        sample_barcode = request.get_assigned_value('sample_barcode')
        query_tuple = (str(sample_barcode),)
        query_str = SamplesAnnotationsQueryBuilder().build_query()

        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)

            # build annotation message
            cursor.execute(query_str, query_tuple)
            rows = cursor.fetchall()
            if len(rows) == 0:
                cursor.close()
                db.close()
                logger.warn("Sample barcode {} not found in metadata_annotation table.".format(sample_barcode))
                raise endpoints.NotFoundException("Sample barcode {} not found".format(sample_barcode))

            items = []
            for row in rows:
                constructor_dict = build_constructor_dict_for_message(MetadataAnnotationItem(), row)
                items.append(MetadataAnnotationItem(**constructor_dict))

            return MetadataAnnotationList(items=items, count=len(items))

        except (IndexError, TypeError), e:
            logger.info("Patient {} not found. Error: {}".format(sample_barcode, e))
            raise endpoints.NotFoundException("Patient {} not found.".format(sample_barcode))
        except MySQLdb.ProgrammingError as e:
            logger.warn("Error retrieving patient data: {}".format(e))
            raise endpoints.BadRequestException("Error retrieving patient data: {}".format(e))
        finally:
            if cursor: cursor.close()
            if db and db.open: db.close()
            request_finished.send(self)