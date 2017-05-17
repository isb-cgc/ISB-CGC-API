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

    @staticmethod
    def build_query(item_type_name=None):
        query_str = 'select * ' \
                    'from metadata_annotation ' \
                    'where SampleBarcode=%s'
        if len(item_type_name) > 0:
            query_str += 'and itemTypeName in (' + ', '.join(['%s']*len(item_type_name)) + ')'

        return query_str

    @staticmethod
    def build_metadata_samples_query():
        query_str = 'select * ' \
                    'from metadata_samples ' \
                    'where sample_barcode=%s '

        return query_str


@ISB_CGC_Endpoints.api_class(resource_name='samples')
class SamplesAnnotationAPI(remote.Service):

    GET_RESOURCE = endpoints.ResourceContainer(sample_barcode=messages.StringField(1, required=True),
                                               item_type_name=messages.StringField(2, repeated=True))

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
        # check to make sure sample_barcode is in correct form
        try:
            parts = sample_barcode.split('-')
            assert len(parts) == 4
            assert len(parts[0]) == 4
            assert len(parts[1]) == 2
            assert len(parts[2]) == 4
            assert len(parts[3]) == 3
        except AssertionError:
            raise endpoints.BadRequestException('{} is not the correct format for a sample barcode. '
                                                'Sample barcodes must be of the form XXXX-XX-XXXX-XXX'.format(sample_barcode))

        item_type_name = request.get_assigned_value('item_type_name')
        # check to make sure item_type_name is valid
        # check to make sure each item_type_name is valid
        if len(item_type_name) > 0:
            for itm in item_type_name:
                itm = itm.strip()
                if itm.lower() not in ['patient', 'aliquot', 'analyte', 'shipped portion', 'portion', 'slide', 'sample']:
                    raise endpoints.BadRequestException("'{}' is not a valid entry for item_type_name. "
                                                        "Valid entries include 'Patient', 'Aliquot', 'Analyte', 'Shipped Portion', "
                                                        "'Portion', 'Slide', and 'Sample'".format(itm))
                query_tuple += (itm,)

        query_str = SamplesAnnotationsQueryBuilder().build_query(item_type_name=item_type_name)
        metadata_samples_query_str = SamplesAnnotationsQueryBuilder().build_metadata_samples_query()

        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)

            # build annotation message
            cursor.execute(query_str, query_tuple)
            rows = cursor.fetchall()
            cursor.execute(metadata_samples_query_str, (str(sample_barcode),))
            metadata_sample_rows = cursor.fetchall()
            if len(rows) == 0:
                cursor.close()
                db.close()
                if len(metadata_sample_rows) == 0:
                    msg = "Sample barcode {} not found in the database.".format(sample_barcode)
                    logger.info(msg)
                else:
                    msg = "No annotations found for sample barcode {}".format(sample_barcode)
                    if item_type_name is not None:
                        msg += " and item type name {}. Item type name must be one of the following: " \
                               "'Patient', 'Aliquot', 'Analyte', 'Shipped Portion', 'Portion', 'Slide', 'Sample'.".format(item_type_name)
                    logger.info(msg)
                raise endpoints.NotFoundException(msg)

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