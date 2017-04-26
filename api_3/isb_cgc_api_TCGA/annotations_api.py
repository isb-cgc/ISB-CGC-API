'''
Created on Mar 23, 2017

Copyright 2017, Institute for Systems Biology

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@author: michael
'''
import MySQLdb

import endpoints
from django.core.signals import request_finished
from protorpc import remote, messages

from api_3.cohort_endpoint_helpers import build_constructor_dict_for_message
from api_3.isb_cgc_api_TCGA.message_classes import MetadataAnnotationItem
from api_3.api_helpers import sql_connection

class MetadataAnnotationList(messages.Message):
    items = messages.MessageField(MetadataAnnotationItem, 1, repeated=True)
    count = messages.IntegerField(2, variant=messages.Variant.INT32)

class AnnotationAPI(remote.Service):
    def process_annotations(self, request, barcode_type, annotationQueryBuilder, logger):
        """
        Base class method to return TCGA annotations about a specific case, sample, or aliquot,
        Takes a barcode as a required parameter.  User does not need to be authenticated.
        """
        try:
            cursor = None
            db = None
            request_barcode = request.get_assigned_value(barcode_type)
            query_tuple = str(request_barcode), 
            try:
                self.validate_barcode(request_barcode)
            except AssertionError:
                raise endpoints.BadRequestException(
                    '{0} is not the correct format for the {1} barcode.'.format(request_barcode, barcode_type))
            entity_types = request.get_assigned_value('entity_type')

            # check to make sure each entity type is valid
            if len(entity_types) > 0:
                for itm in entity_types:
                    itm = itm.strip()
                    if itm.lower() not in ['case', 'aliquot', 'analyte', 'portion', 'slide', 'sample']:
                        raise endpoints.BadRequestException("'{}' is not a valid entry for entity_type. "
                            "Valid entries are 'case', 'aliquot', 'analyte', 'portion', 'slide', and 'sample'".
                            format(itm))
                    query_tuple += itm, 
            
            query_str = annotationQueryBuilder.build_query(entity_types=entity_types)
            metadata_query_str = annotationQueryBuilder.build_metadata_query()
            db = sql_connection()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
        # build annotation message
            cursor.execute(query_str, query_tuple)
            rows = cursor.fetchall()
            cursor.execute(metadata_query_str, (str(request_barcode), ))
            metadata_rows = cursor.fetchall()
            if len(rows) == 0:
                cursor.close()
                db.close()
                if len(metadata_rows) == 0:
                    msg = "{} {} not found in the database.".format(barcode_type, request_barcode)
                    logger.info(msg)
                else:
                    msg = "No annotations found for {} {}".format(barcode_type, request_barcode)
                    if entity_types is not None and 0 < len(entity_types):
                        msg += " and entity_type {}. entity_type name must be one of the following: "\
                        "'case', 'aliquot', 'analyte', 'portion', 'slide', 'sample'.".format(entity_types)
                    logger.info(msg)
                raise endpoints.NotFoundException(msg)
            items = []
            for row in rows:
                constructor_dict = build_constructor_dict_for_message(MetadataAnnotationItem(), row)
                items.append(MetadataAnnotationItem(**constructor_dict))
            
            return MetadataAnnotationList(items=items, count=len(items))

        except (IndexError, TypeError), e:
            logger.info("{} {} not found. Error: {}".format(barcode_type, request_barcode, e))
            raise endpoints.NotFoundException("{} {} not found.".format(barcode_type, request_barcode))
        except MySQLdb.ProgrammingError as e:
            logger.warn("Error retrieving {} data: {}".format(barcode_type, e))
            raise endpoints.BadRequestException("Error retrieving {} data: {}".format(barcode_type, e))
        finally:
            if cursor: cursor.close()
            if db and db.open: db.close()
            request_finished.send(self)
