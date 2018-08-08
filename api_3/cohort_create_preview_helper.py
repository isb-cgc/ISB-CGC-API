'''
Created on Mar 30, 2017

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
import django
import re
import endpoints
import logging
import MySQLdb
from protorpc import remote, messages
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.models import User as Django_User
from django.core.signals import request_finished
from api_3.cohort_endpoint_helpers import are_there_bad_keys, are_there_no_acceptable_keys, construct_parameter_error_message

from api_3.api_helpers import sql_connection, WHITELIST_RE
from bq_data_access.cohort_bigquery import BigQueryCohortSupport
from cohorts.models import Cohort as Django_Cohort, Cohort_Perms, Samples, Filters
from projects.models import Program, Project

logger = logging.getLogger(__name__)

class CohortsCreatePreviewAPI(remote.Service):
    def build_query_dictionaries(self, request):
        """
        Builds the query dictionaries for create and preview cohort endpoints.
        Returns query_dict, gte_query_dict, lte_query_dict.
        """
        query_dict = {
            k.name: request.get_assigned_value(k.name)
            for k in request.all_fields()
            if request.get_assigned_value(k.name)
            and k.name is not 'name'
            and not k.name.endswith('_gte')
            and not k.name.endswith('_lte')
            }

        gte_query_dict = {
            k.name.replace('_gte', ''): request.get_assigned_value(k.name)
            for k in request.all_fields()
            if request.get_assigned_value(k.name) and k.name.endswith('_gte')
            }

        lte_query_dict = {
            k.name.replace('_lte', ''): request.get_assigned_value(k.name)
            for k in request.all_fields()
            if request.get_assigned_value(k.name) and k.name.endswith('_lte')
            }

        return query_dict, gte_query_dict, lte_query_dict

    def build_query(self, program, table, query_dict, gte_query_dict, lte_query_dict):
        """
        Builds the queries that selects the case and sample barcodes
        that meet the criteria specified in the request body.
        Returns case query string,  sample query string, value tuple.
        """
        if (0 == len(query_dict) and 0 == len(gte_query_dict) and 0 == len(lte_query_dict)):
            return None, None
        
        if 'Clinical' == table:
            query_str = 'SELECT sample_barcode, c.case_barcode, c.project_short_name ' \
                               'FROM {0}_metadata_clinical c join {0}_metadata_biospecimen b on c.case_barcode = b.case_barcode ' \
                               'WHERE '.format(program)
        else:
            query_str = 'SELECT sample_barcode, case_barcode, project_short_name ' \
                               'FROM {0}_metadata_{1} ' \
                               'WHERE '.format(program, table[:1].lower() + table[1:])
        value_tuple = ()

        alias = 'c.' if 'Clinical' == table else ''
        for key, value_list in query_dict.iteritems():
            query_str += ' AND ' if not query_str.endswith('WHERE ') else ''
            if "None" in value_list:
                value_list.remove("None")
                query_str += ' ( {alias}{key} is null '.format(alias=alias, key=key)
                if len(value_list) > 0:
                    query_str += ' OR {alias}{key} IN ({vals}) '.format(
                        alias=alias, key=key, vals=', '.join(['%s'] * len(value_list)))
                query_str += ') '
            else:
                query_str += ' {alias}{key} IN ({vals}) '.format(alias=alias, key=key, vals=', '.join(['%s'] * len(value_list)))
            value_tuple += tuple(value_list)

        for key, value in gte_query_dict.iteritems():
            query_str += ' AND ' if not query_str.endswith('WHERE ') else ''
            query_str += ' {}{} >=%s '.format(alias, key)
            value_tuple += (value,)

        for key, value in lte_query_dict.iteritems():
            query_str += ' AND ' if not query_str.endswith('WHERE ') else ''
            query_str += ' {}{} <=%s '.format(alias, key)
            value_tuple += (value,)

        query_str += ' GROUP BY sample_barcode, {0}case_barcode, {0}project_short_name'.format(alias)

        return query_str, value_tuple

    def query(self, request):
        try:
            db = None
            try:
                db = sql_connection()
            except Exception as e:
                logger.exception(e)
                raise endpoints.NotFoundException("Error connecting to database: {}".format(e))
            
            fields = request.get_assigned_value('Common')
            common_query_dict = {}

            if fields:
                common_query_dict, _, _ = self.build_query_dictionaries(fields)

            # Our return values
            ret_query_dict = {}
            ret_lte_query_dict = {}
            ret_gte_query_dict = {}
            ret_rows = None

            for table in ('Clinical', 'Biospecimen', 'Data_HG19', 'Data_HG38'):
                if 'CCLE' == self.program and 'Data_HG38' == table:
                    continue

                fields = request.get_assigned_value(table)

                if fields and (are_there_bad_keys(fields) or are_there_no_acceptable_keys(fields)):
                    err_msg = construct_parameter_error_message(request, True)
                    raise endpoints.BadRequestException(err_msg)

                query_dict = {}
                gte_query_dict = {}
                lte_query_dict = {}

                if fields:
                    query_dict, gte_query_dict, lte_query_dict = self.build_query_dictionaries(fields)

                logger.info("query_dict: {}".format(str(query_dict)))
                logger.info("common_query_dict: {}".format(str(common_query_dict)))
                    
                query_dict.update(common_query_dict)

                ret_query_dict.update(query_dict)
                ret_lte_query_dict.update(lte_query_dict)
                ret_gte_query_dict.update(gte_query_dict)

                query_str, value_tuple = self.build_query(self.program, table, query_dict, gte_query_dict, lte_query_dict)

                if not query_str:
                    continue

                cursor = None
                try:
                    cursor = db.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute(query_str, value_tuple)
                    rows = list(cursor.fetchall())
                    if 0 == len(rows):
                        # if any query returns no rows, then, overall, no sample_barcode will match
                        return [], '', '', ''
                        
                    if ret_rows is None:
                        ret_rows = rows
                    else:
                        cur_samples = set()
                        for row in rows:
                            cur_samples.add(row['sample_barcode'])
                        not_in_sample = []
                        for row in ret_rows:
                            if row['sample_barcode'] not in cur_samples:
                                not_in_sample += [row]
                        for row in not_in_sample:
                            ret_rows.remove(row)
                except (IndexError, TypeError) as e:
                    logger.exception(e)
                    raise endpoints.NotFoundException("Error retrieving samples and cases: {}\n{} {}".format(e, query_str, value_tuple))
                except MySQLdb.ProgrammingError as e:
                    msg = '{}:\n\tsample query: {} {}'.format(e, query_str, value_tuple)
                    logger.exception(msg)
                    raise endpoints.BadRequestException("Error creating/previewing cohort. {}".format(e))
                finally:
                    if cursor:
                        cursor.close()
        finally:
            if db and db.open:
                db.close()
            request_finished.send(self)
        
        return ret_rows, ret_query_dict, ret_lte_query_dict, ret_gte_query_dict
    
class FilterDetails(messages.Message):
    name = messages.StringField(1)
    value = messages.StringField(2)

class CreatedCohort(messages.Message):
    id = messages.StringField(1)
    name = messages.StringField(2)
    last_date_saved = messages.StringField(3)
    filters = messages.MessageField(FilterDetails, 4, repeated=True)
    case_count = messages.IntegerField(5, variant=messages.Variant.INT32)
    sample_count = messages.IntegerField(6, variant=messages.Variant.INT32)

class CohortsCreateHelper(CohortsCreatePreviewAPI):
    BASE_URL = settings.BASE_URL
    
    def get_django_program(self, program_name):
        try:
            # get the ISB superuser
            isb_superuser = Django_User.objects.get(username='isb', is_staff=True, is_superuser=True, is_active=True)
            # get the program
            program = Program.objects.get(name=program_name, is_public=True, active=True, owner=isb_superuser)
        finally:
            request_finished.send(self)
        return program

    def get_django_project(self, project_short_name):
        try:
            # get the ISB superuser
            isb_superuser = Django_User.objects.get(username='isb', is_staff=True, is_superuser=True, is_active=True)
            # get the program
            program = self.get_django_program(project_short_name.split('-')[0])
            # get the project
            project = Project.objects.get(name=project_short_name[project_short_name.find('-') + 1:], active=True, owner=isb_superuser, program=program)
        finally:
            request_finished.send(self)
        return project

    def create(self, request):
        """
        Creates and saves a cohort. Takes a JSON object in the request body to use as the cohort's filters.
        Authentication is required.
        Returns information about the saved cohort, including the number of cases and the number
        of samples in that cohort.
        """
        user = endpoints.get_current_user()
        user_email = user.email() if user else None

        if user_email is None:
            raise endpoints.UnauthorizedException(
                "Authentication failed. Try signing in to {} to register "
                "with the web application.".format(self.BASE_URL))

        django.setup()
        try:
            django_user = Django_User.objects.get(email=user_email)
        except (ObjectDoesNotExist, MultipleObjectsReturned), e:
            logger.warn(e)
            raise endpoints.NotFoundException("%s does not have an entry in the user database." % user_email)
        finally:
            request_finished.send(self)

        # get the sample barcode information for use in creating the sample list for the cohort
        rows, query_dict, lte_query_dict, gte_query_dict = self.query(request)
        project2django = {}
        if rows:
            for row in rows:
                if row['project_short_name'] not in project2django:
                    project2django[row['project_short_name']] = self.get_django_project(row['project_short_name'])
        else:
            raise endpoints.BadRequestException("No samples meet the specified parameters.")

        sample_barcodes = [{'sample_barcode': row['sample_barcode'], 'case_barcode': row['case_barcode'], 'project': project2django[row['project_short_name']]} for row in rows]
        cohort_name = request.get_assigned_value('name')

        # Validate the cohort name against a whitelist
        whitelist = re.compile(WHITELIST_RE, re.UNICODE)
        match = whitelist.search(unicode(cohort_name))
        if match:
            # XSS risk, log and fail this cohort save
            match = whitelist.findall(unicode(cohort_name))
            logger.error(
                '[ERROR] While saving a cohort, saw a malformed name: ' + cohort_name + ', characters: ' + match.__str__())
            raise endpoints.BadRequestException(
                "Your cohort's name contains invalid characters (" + match.__str__() + "); please choose another name.")

        if len(sample_barcodes) == 0:
            raise endpoints.BadRequestException(
                "The cohort could not be saved because no samples meet the specified parameters.")

        # todo: maybe create all objects first, then save them all at the end?
        # 1. create new cohorts_cohort with name, active=True, last_date_saved=now
        try:
            created_cohort = Django_Cohort.objects.create(name=cohort_name, active=True, last_date_saved=datetime.utcnow())
            created_cohort.save()
        finally:
            request_finished.send(self)

        # 2. insert samples into cohort_samples
        try:
            sample_list = [Samples(cohort=created_cohort, sample_barcode=sample['sample_barcode'], case_barcode=sample['case_barcode'], project=sample['project']) for sample in sample_barcodes]
            Samples.objects.bulk_create(sample_list)
        finally:
            request_finished.send(self)

        # 3. Set permission for user to be owner
        try:
            perm = Cohort_Perms(cohort=created_cohort, user=django_user, perm=Cohort_Perms.OWNER)
            perm.save()
        finally:
            request_finished.send(self)

        # 4. Create filters applied
        filter_data = []
        django_program = self.get_django_program(self.program)
        try:
            # special case sample barcode since the list can be ALL the sample barcodes in the program
            edit_barcodes = set()
            for key, value_list in query_dict.items():
                if 'sample_barcode' == key:
                    edit_barcodes |= set(value_list)
                    continue
                for val in value_list:
                    filter_data.append(FilterDetails(name=key, value=str(val)))
                    Filters.objects.create(resulting_cohort=created_cohort, name=key, value=val, program=django_program).save()
            if 0 < len(edit_barcodes):
                if len(edit_barcodes) < 6:
                    val = 'barcodes: {}'.format(', '.join(sorted(list(edit_barcodes))))
                else:
                    val = '{} barcodes beginning with {}'.format(len(edit_barcodes), ', '.join(sorted(list(edit_barcodes))[:5]))
                filter_data.append(FilterDetails(name='sample_barcode', value=val))
                Filters.objects.create(resulting_cohort=created_cohort, name='sample_barcode', value=val, program=django_program).save()
    
            for key, val in [(k + '_lte', v) for k, v in lte_query_dict.items()] + [(k + '_gte', v) for k, v in gte_query_dict.items()]:
                filter_data.append(FilterDetails(name=key, value=str(val)))
                Filters.objects.create(resulting_cohort=created_cohort, name=key, value=val, program=django_program).save()
        finally:
            request_finished.send(self)

        # 5. Store cohort to BigQuery
        project_id = settings.BQ_PROJECT_ID
        cohort_settings = settings.GET_BQ_COHORT_SETTINGS()
        bcs = BigQueryCohortSupport(project_id, cohort_settings.dataset_id, cohort_settings.table_id)
        batch = 5000
        start = 0
        while start < len(sample_barcodes):
            bcs.add_cohort_to_bq(created_cohort.id, sample_barcodes[start:start + batch])
            start += batch

        request_finished.send(self)

        return CreatedCohort(
            id=str(created_cohort.id),
            name=cohort_name,
            last_date_saved=str(datetime.utcnow()),
            filters=filter_data,
            case_count=created_cohort.case_size(),
            sample_count=len(sample_barcodes)
        )
    
class CohortsPreviewHelper(CohortsCreatePreviewAPI):
    class CohortCasesSamplesList(messages.Message):
        cases = messages.StringField(1, repeated=True)
        case_count = messages.IntegerField(2, variant=messages.Variant.INT32)
        samples = messages.StringField(3, repeated=True)
        sample_count = messages.IntegerField(4, variant=messages.Variant.INT32)
    
    def preview(self, request):
        """
        Takes a JSON object of filters in the request body and returns a "preview" of the cohort that would
        result from passing a similar request to the cohort **save** endpoint.  This preview consists of
        two lists: the lists of case barcodes, and the list of sample barcodes.
        Authentication is not required.
        """
        rows, _, _, _ = self.query(request)

        case_barcodes = set()
        sample_barcodes = []

        if rows:
            for row in rows:
                case_barcodes.add(row['case_barcode'])
                sample_barcodes.append(row['sample_barcode'])
            case_barcodes = list(case_barcodes)

        if len(sample_barcodes) == 0:
            raise endpoints.BadRequestException("No samples meet the specified parameters.")

        return self.CohortCasesSamplesList(cases=case_barcodes,
                                         case_count=len(case_barcodes),
                                         samples=sample_barcodes,
                                         sample_count=len(sample_barcodes))
