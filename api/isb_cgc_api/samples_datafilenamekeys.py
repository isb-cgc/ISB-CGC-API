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
from django.core.signals import request_finished
from protorpc import remote, messages

from isb_cgc_api_helpers import ISB_CGC_Endpoints, are_there_bad_keys, construct_parameter_error_message
from api.api_helpers import sql_connection

logger = logging.getLogger(__name__)


class DataFileNameKeyList(messages.Message):
    datafilenamekeys = messages.StringField(1, repeated=True)
    count = messages.IntegerField(2)


@ISB_CGC_Endpoints.api_class(resource_name='samples')
class SamplesDatafilenamekeysAPI(remote.Service):

    GET_RESOURCE = endpoints.ResourceContainer(sample_barcode=messages.StringField(1, required=True),
                                               platform=messages.StringField(2),
                                               pipeline=messages.StringField(3))

    @endpoints.method(GET_RESOURCE, DataFileNameKeyList,
                      path='samples/{sample_barcode}/datafilenamekeys', http_method='GET')
    def datafilenamekeys(self, request):
        """
        Takes a sample barcode as a required parameter and
        returns cloud storage paths to files associated with that sample.
        """
        cursor = None
        db = None

        sample_barcode = request.get_assigned_value('sample_barcode')
        platform = request.get_assigned_value('platform')
        pipeline = request.get_assigned_value('pipeline')

        if are_there_bad_keys(request):
            err_msg = construct_parameter_error_message(request, False)
            raise endpoints.BadRequestException(err_msg)

        query_str = 'SELECT DataFileNameKey, SecurityProtocol, Repository ' \
                    'FROM metadata_data WHERE SampleBarcode=%s '

        query_tuple = (sample_barcode,)

        if platform:
            query_str += ' and Platform=%s '
            query_tuple += (platform,)

        if pipeline:
            query_str += ' and Pipeline=%s '
            query_tuple += (pipeline,)

        query_str += ' GROUP BY DataFileNameKey, SecurityProtocol, Repository'

        try:
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query_str, query_tuple)

            datafilenamekeys = []
            bad_repo_count = 0
            bad_repo_set = set()
            for row in cursor.fetchall():
                if not row.get('DataFileNameKey'):
                    continue
                if 'controlled' not in str(row['SecurityProtocol']).lower():
                    datafilenamekeys.append("gs://{}{}".format(settings.OPEN_DATA_BUCKET, row.get('DataFileNameKey')))
                else:  # not filtering on dbGaP_authorized
                    bucket_name = ''
                    if row['Repository'].lower() == 'dcc':
                        bucket_name = settings.DCC_CONTROLLED_DATA_BUCKET
                    elif row['Repository'].lower() == 'cghub':
                        bucket_name = settings.CGHUB_CONTROLLED_DATA_BUCKET
                    else:  # shouldn't ever happen
                        bad_repo_count += 0
                        bad_repo_set.add(row['Repository'])
                        continue
                    datafilenamekeys.append("gs://{}{}".format(bucket_name, row.get('DataFileNameKey')))
            if bad_repo_count > 0:
                logger.warn("not returning {count} row(s) in sample_details due to repositories: {bad_repo_list}"
                            .format(count=bad_repo_count, bad_repo_list=list(bad_repo_set)))
            return DataFileNameKeyList(datafilenamekeys=datafilenamekeys, count=len(datafilenamekeys))

        except (IndexError, TypeError), e:
            logger.warn(e)
            raise endpoints.NotFoundException("File paths for sample {} not found.".format(sample_barcode))
        except MySQLdb.ProgrammingError as e:
            msg = '{}:\n\t query: {} {}'.format(e, query_str, query_tuple)
            logger.warn(msg)
            raise endpoints.BadRequestException("Error retrieving file paths. {}".format(msg))
        finally:
            if cursor: cursor.close()
            if db and db.open: db.close()
            request_finished.send(self)