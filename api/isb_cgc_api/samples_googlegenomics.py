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

from django.conf import settings
from protorpc import remote, messages

from isb_cgc_api_helpers import ISB_CGC_Endpoints, are_there_bad_keys, construct_parameter_error_message
from api.api_helpers import sql_connection

logger = logging.getLogger(__name__)

BASE_URL = settings.BASE_URL


class GoogleGenomics(messages.Message):
    SampleBarcode = messages.StringField(1)
    GG_dataset_id = messages.StringField(2)
    GG_readgroupset_id = messages.StringField(3)


class GoogleGenomicsList(messages.Message):
    items = messages.MessageField(GoogleGenomics, 1, repeated=True)
    count = messages.IntegerField(2)


@ISB_CGC_Endpoints.api_class(resource_name='samples')
class SamplesGoogleGenomicsAPI(remote.Service):

    GET_RESOURCE = endpoints.ResourceContainer(sample_barcode=messages.StringField(1, required=True))

    @endpoints.method(GET_RESOURCE, GoogleGenomicsList, http_method='GET',
                      path='samples/{sample_barcode}/googlegenomics')
    def googlegenomics(self, request):
        """
        Takes a sample barcode as a required parameter and returns the Google Genomics dataset id
        and readgroupset id associated with the sample, if any.
        """
        # print >> sys.stderr,'Called '+sys._getframe().f_code.co_name
        cursor = None
        db = None
        sample_barcode = request.get_assigned_value('sample_barcode')

        if are_there_bad_keys(request):
            err_msg = construct_parameter_error_message(request, False)
            raise endpoints.BadRequestException(err_msg)

        query_str = 'SELECT SampleBarcode, GG_dataset_id, GG_readgroupset_id ' \
                    'FROM metadata_data ' \
                    'WHERE SampleBarcode=%s ' \
                    'AND GG_dataset_id !="" AND GG_readgroupset_id !="" ' \
                    'GROUP BY SampleBarcode, GG_dataset_id, GG_readgroupset_id;'

        query_tuple = (sample_barcode,)
        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query_str, query_tuple)

            google_genomics_items = []
            for row in cursor.fetchall():
                google_genomics_items.append(
                    GoogleGenomics(
                        SampleBarcode=row['SampleBarcode'],
                        GG_dataset_id=row['GG_dataset_id'],
                        GG_readgroupset_id=row['GG_readgroupset_id']
                    )
                )

            return GoogleGenomicsList(items=google_genomics_items, count=len(google_genomics_items))

        except (IndexError, TypeError), e:
            logger.warn(e)
            raise endpoints.NotFoundException(
                "Google Genomics dataset and readgroupset id's for sample {} not found."
                    .format(sample_barcode))
        except MySQLdb.ProgrammingError as e:
            msg = '{}:\n\tquery: {} {}' \
                .format(e, query_str, query_tuple)
            logger.warn(msg)
            raise endpoints.BadRequestException("Error retrieving genomics data for sample. {}".format(msg))
        finally:
            if cursor: cursor.close()
            if db and db.open: db.close()