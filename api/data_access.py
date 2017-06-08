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

import logging
import json
import math
import traceback

from endpoints import api as endpoints_api, method as endpoints_method
from endpoints import NotFoundException, InternalServerErrorException
from protorpc import remote
from protorpc.messages import BooleanField, EnumField, IntegerField, Message, MessageField, StringField

from bq_data_access.feature_value_types import ValueType, is_log_transformable
from bq_data_access.data_access import is_valid_feature_identifier, get_feature_vectors_tcga_only, get_feature_vectors_with_user_data
from bq_data_access.utils import VectorMergeSupport
from bq_data_access.cohort_cloudsql import CloudSQLCohortAccess
from bq_data_access.utils import DurationLogged
from bq_data_access.data_access import FeatureIdQueryDescription

from api.pairwise import PairwiseInputVector, Pairwise
from api.pairwise_api import PairwiseResults, PairwiseResultVector, PairwiseFilterMessage
from api.api_helpers import sql_connection

from projects.models import Project

import sys

logger = logging.getLogger(__name__)

VIZ_UNIT_DATADICTIONARY = {
    'BMI': 'kg/m^2',
}

ISB_CGC_PROJECTS = {
    'list': []
}

# DUPLICATE METHOD
# Due to the way sql connections are done, it's easiest to duplicate this method and the static variable
# it creates. The original is in Cohorts/views, and all changes will happen there first.
#
# Generate the ISB_CGC_PROJECTS['list'] value set based on the get_isbcgc_project_set sproc
def fetch_isbcgc_project_set():
    try:
        cursor = None
        db = sql_connection()
        if not ISB_CGC_PROJECTS['list'] or len(ISB_CGC_PROJECTS['list']) <= 0:
            cursor = db.cursor()
            cursor.execute("SELECT COUNT(SPECIFIC_NAME) FROM INFORMATION_SCHEMA.ROUTINES WHERE SPECIFIC_NAME = 'get_isbcgc_project_set';")
            # Only try to fetch the study set if the sproc exists
            if cursor.fetchall()[0][0] > 0:
                cursor.execute("CALL get_isbcgc_project_set();")
                ISB_CGC_PROJECTS['list'] = []
                for row in cursor.fetchall():
                    ISB_CGC_PROJECTS['list'].append(row[0])
            else:
                # Otherwise just warn
                logger.warn("[WARNING] Stored procedure get_isbcgc_project_set was not found!")

        return ISB_CGC_PROJECTS['list']
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())
    finally:
        if cursor: cursor.close()
        if db and db.open: db.close()


def get_axis_units(xAttr, yAttr):
    units = {'x': '', 'y': ''}

    checkUnits = {}
    if xAttr is not None:
        checkUnits[xAttr] = 'x'
    if yAttr is not None:
        checkUnits[yAttr] = 'y'

    for attr in checkUnits:

        if '_age' in attr or 'age_' in attr or 'year_' in attr:
            units[checkUnits[attr]] = 'years'
        elif '_days' in attr or 'days_' in attr:
            units[checkUnits[attr]] = 'days'
        elif 'percent' in attr:
            units[checkUnits[attr]] = 'percent'
        elif 'CNVR:' in attr:
            units[checkUnits[attr]] = 'log(CN/2)'
        elif 'RPPA:' in attr:
            units[checkUnits[attr]] = 'protein expression'
        elif 'METH:' in attr:
            units[checkUnits[attr]] = 'beta value'
        elif 'GEXP:' in attr or 'MIRN:' in attr or ('GNAB:' in attr and "num_mutations" in attr):
            units[checkUnits[attr]] = 'count'
        elif attr.split(':')[1] in VIZ_UNIT_DATADICTIONARY:
            units[checkUnits[attr]] = VIZ_UNIT_DATADICTIONARY[attr.split(':')[1]]

    return units


class DataRequest(Message):
    feature_id = StringField(1, required=True)
    cohort_id = IntegerField(2, required=True)


class DataPoint(Message):
    patient_id = StringField(1)
    sample_id = StringField(2)
    aliquot_id = StringField(3)
    value = StringField(4)


class DataPointList(Message):
    type = EnumField(ValueType, 1)
    items = MessageField(DataPoint, 2, repeated=True)


class PlotDataRequest(Message):
    x_id = StringField(1, required=True)
    y_id = StringField(2, required=False)
    c_id = StringField(3, required=False)
    log_transform = StringField(4, required=False)
    cohort_id = IntegerField(5, repeated=True)
    pairwise = BooleanField(6, required=False)


class PlotDataPointCohortMemberships(Message):
    ids = IntegerField(1, repeated=True)


class PlotDataCohortInfo(Message):
    id = IntegerField(1, required=True)
    name = StringField(2, required=True)

DATAPOINT_COHORT_THRESHOLD = 1


class PlotDataPoint(Message):
    sample_id = StringField(1)
    case_id = StringField(2)
    x = StringField(3)
    y = StringField(4)
    c = StringField(5)
    cohort = IntegerField(6, repeated=True)


class PlotDataTypes(Message):
    x = EnumField(ValueType, 1)
    y = EnumField(ValueType, 2)
    c = EnumField(ValueType, 3)


class PlotDataFeatureLabels(Message):
    x = StringField(1)
    y = StringField(2)
    c = StringField(3)


class PlotDatapointCohortSet(Message):
    datapoint_id = StringField(1, required=True)


class PlotDatapointCount(Message):
    total_num_patients = IntegerField(1, required=True)
    total_num_samples = IntegerField(2, required=True)
    num_patients_w_xy = IntegerField(3, required=True)
    num_samples_w_xy = IntegerField(4, required=True)
    num_patients_wo_x = IntegerField(5, required=True)
    num_samples_wo_x = IntegerField(6, required=True)
    num_patients_wo_y = IntegerField(7, required=True)
    num_samples_wo_y = IntegerField(8, required=True)


class PlotDataResponse(Message):
    types = MessageField(PlotDataTypes, 1, required=True)
    labels = MessageField(PlotDataFeatureLabels, 2, required=True)
    items = MessageField(PlotDataPoint, 3, repeated=True)
    cohort_set = MessageField(PlotDataCohortInfo, 4, repeated=True)
    counts = MessageField(PlotDatapointCount, 5)
    pairwise_result = MessageField(PairwiseResults, 6, required=False)
    xUnits = StringField(7, required=False)
    yUnits = StringField(8, required=False)


FeatureDataEndpointsAPI = endpoints_api(name='feature_data_api', version='v1',
                                        description='Endpoints for feature data used by the web application.')


@FeatureDataEndpointsAPI.api_class(resource_name='feature_data_endpoints')
class FeatureDataEndpoints(remote.Service):
    def get_counts(self, data):
        total_num_patients = []
        total_num_samples = []
        num_samples_w_xy = []
        num_patients_w_xy = []
        num_samples_wo_x = []
        num_samples_wo_y = []
        num_patients_wo_x = []
        num_patients_wo_y = []

        result = {}

        for item in data:
            total_num_samples.append(item['sample_id'])
            total_num_patients.append(item['sample_id'][:12])

            if item['x'] != 'NA' and item['y'] != 'NA':
                num_samples_w_xy.append(item['sample_id'])
                num_patients_w_xy.append(item['sample_id'][:12])
            else:
                if item['x'] == 'NA':
                    num_samples_wo_x.append(item['sample_id'])
                    if item['sample_id'][:12] not in num_patients_w_xy:
                        num_patients_wo_x.append(item['sample_id'][:12])
                elif item['y'] == 'NA':
                    num_samples_wo_y.append(item['sample_id'])
                    if item['sample_id'][:12] not in num_patients_w_xy:
                        num_patients_wo_y.append(item['sample_id'][:12])

        result['total_num_patients'] = len(set(total_num_patients))
        result['total_num_samples'] = len(set(total_num_samples))
        result['num_patients_w_xy'] = len(set(num_patients_w_xy))
        result['num_samples_w_xy'] = len(set(num_samples_w_xy))
        result['num_patients_wo_x'] = len(set(num_patients_wo_x))
        result['num_samples_wo_x'] = len(set(num_samples_wo_x))
        result['num_patients_wo_y'] = len(set(num_patients_wo_y))
        result['num_samples_wo_y'] = len(set(num_samples_wo_y))

        return result

    # TODO refactor to separate module
    @DurationLogged('PAIRWISE', 'GET')
    def get_pairwise_result(self, feature_array):
        # Format the feature vectors for pairwise
        input_vectors = Pairwise.prepare_feature_vector(feature_array)
        outputs = None
        results = None

        try:
            outputs = Pairwise.run_pairwise(input_vectors)

            if outputs is not None:
                results = PairwiseResults(result_vectors=[], filter_messages=[])
                for row_label, row in outputs.items():
                    if type(row) is dict:
                        results.result_vectors.append(PairwiseResultVector(feature_1=row['feature_A'],
                                                                           feature_2=row['feature_B'],
                                                                           comparison_type=row['comparison_type'],
                                                                           correlation_coefficient=row['correlation_coefficient'],
                                                                           n=int(row['n']),
                                                                           _logp=float(row['_logp']),
                                                                           n_A=int(row['n_A']),
                                                                           p_A=float(row['p_A']),
                                                                           n_B=int(row['n_B']),
                                                                           p_B=float(row['p_B']),
                                                                           exclusion_rules=row['exclusion_rules']))
                    elif type(row) is unicode:
                        results.filter_messages.append(PairwiseFilterMessage(filter_message=row[0]))
        except Exception as e:
            outputs = None
            results = None
            logger.error(traceback.format_exc())

        return results

    @DurationLogged('FEATURE', 'VECTOR_MERGE')
    def get_merged_dict_timed(self, vms):
        return vms.get_merged_dict()

    # TODO refactor missing value logic out of this module
    @DurationLogged('FEATURE', 'GET_VECTORS')
    def get_merged_feature_vectors(self, x_id, y_id, c_id, cohort_id_array, logTransform, study_id_array):
        """
        Fetches and merges data for two or three feature vectors (see parameter documentation below).
        The vectors have to be an array of dictionaries, with each dictionary containing a 'value' field
        (other fields are ignored):
        [
            {
                'value': 0.5
            },
            {
                'value': 1.0
            }
        ]
        The merged result:
        [
            {
                'patient_id': <patient ID #0>
                'x': <value for x for patient ID #0>
                'y': <value for y for patient ID #0>
                'c': <value for c for patient ID #0>
            },
            {
                'patient_id': <patient ID #1>
                'x': <value for x for patient ID #1>
                'y': <value for y for patient ID #1>
                'c': <value for c for patient ID #1>
            }
            ...
        ]

        :param x_id: Feature identifier for x-axis e.g. 'CLIN:age_at_initial_pathologic_diagnosis'
        :param y_id: Feature identifier for y-axis. If None, values for 'y' in the response will be marked as missing.
        :param c_id: Feature identifier for color-by. If None, values for 'c' in the response will be marked as missing.
        :param cohort_id_array: Cohort identifier array.

        :return: PlotDataResponse
        """

        async_params = [FeatureIdQueryDescription(x_id, cohort_id_array, study_id_array)]

        c_type, c_vec = ValueType.STRING, []
        y_type, y_vec = ValueType.STRING, []

        units = get_axis_units(x_id, y_id)

        if c_id is not None:
            async_params.append(FeatureIdQueryDescription(c_id, cohort_id_array, study_id_array))
        if y_id is not None:
            async_params.append(FeatureIdQueryDescription(y_id, cohort_id_array, study_id_array))

        async_result = get_feature_vectors_tcga_only(async_params)

        if c_id is not None:
            c_type, c_vec = async_result[c_id]['type'], async_result[c_id]['data']
        if y_id is not None:
            y_type, y_vec = async_result[y_id]['type'], async_result[y_id]['data']
            if logTransform is not None and logTransform['y'] and y_vec and is_log_transformable(y_type):
                # If we opt to use a transform that attempts to account for values out of range for log transformation,
                # this is the code to get the minimum y-value
                '''
                yvals = []
                for yd in y_vec:
                    if 'value' in yd and yd['value'] is not None and yd['value'] != "NA" and yd['value'] != "None":
                        yvals.append(float(yd['value']))
                y_min = min(yvals)
                '''
                for ydata in y_vec:
                    if 'value' in ydata and ydata['value'] is not None and ydata['value'] != "NA" and ydata['value'] != "None":
                        if float(ydata['value']) < 0:
                            ydata['value'] = "NA"
                        elif logTransform['yBase'] == 10:
                            ydata['value'] = str(math.log10((float(ydata['value']) + 1)))
                        elif logTransform['yBase'] == 'e':
                            ydata['value'] = str(math.log((float(ydata['value']) + 1)))
                        elif type(logTransform['yBase']) is int:
                            ydata['value'] = str(math.log((float(ydata['value']) + 1), logTransform['yBase']))
                        else:
                            logger.warn(
                                "[WARNING] No valid log base was supplied - log transformation will not be applied!"
                            )

        x_type, x_vec = async_result[x_id]['type'], async_result[x_id]['data']

        if logTransform is not None and logTransform['x'] and x_vec and is_log_transformable(x_type):
            # If we opt to use a transform that attempts to account for values out of range for log transformation,
            # this is the code to get the minimum x-value
            '''
            xvals = []
            for xd in x_vec:
                if 'value' in xd and xd['value'] is not None and xd['value'] != "NA" and xd['value'] != "None":
                    xvals.append(float(xd['value']))
            x_min = min(xvals)
            '''

            for xdata in x_vec:
                if 'value' in xdata and xdata['value'] is not None and xdata['value'] != "NA" and xdata['value'] != "None":
                    if float(xdata['value']) < 0:
                        xdata['value'] = "NA"
                    elif logTransform['xBase'] == 10:
                        xdata['value'] = str(math.log10((float(xdata['value']) + 1)))
                    elif logTransform['xBase'] == 'e':
                        xdata['value'] = str(math.log((float(xdata['value']) + 1)))
                    elif type(logTransform['xBase']) is int:
                        xdata['value'] = str(math.log((float(xdata['value']) + 1), logTransform['xBase']))
                    else:
                        logger.warn(
                            "[WARNING] No valid log base was supplied - log transformation will not be applied!"
                        )

        vms = VectorMergeSupport('NA', 'sample_id', 'case_id', ['x', 'y', 'c']) # changed so that it plots per sample not patient
        vms.add_dict_array(x_vec, 'x', 'value')
        vms.add_dict_array(y_vec, 'y', 'value')
        vms.add_dict_array(c_vec, 'c', 'value')
        merged = self.get_merged_dict_timed(vms)

        # Resolve which (requested) cohorts each datapoint belongs to.
        cohort_set_dict = CloudSQLCohortAccess.get_cohorts_for_datapoints(cohort_id_array)

        # Get the name and ID for every requested cohort.
        cohort_info_array = CloudSQLCohortAccess.get_cohort_info(cohort_id_array)
        cohort_info_obj_array = []
        for item in cohort_info_array:
            cohort_info_obj_array.append(PlotDataCohortInfo(id=item['id'], name=item['name']))

        items = []
        for value_bundle in merged:
            sample_id = value_bundle['sample_id']

            # Add an array of cohort
            # only if the number of containing cohort exceeds the configured threshold.
            cohort_set = []
            # TODO FIX - this check shouldn't be needed
            if sample_id in cohort_set_dict:
                cohort_set = cohort_set_dict[sample_id]

            if len(cohort_set) >= DATAPOINT_COHORT_THRESHOLD:
                value_bundle['cohort'] = cohort_set

            items.append(PlotDataPoint(**value_bundle))

        counts = self.get_counts(merged)
        count_message = PlotDatapointCount(**counts)

        type_message = PlotDataTypes(x=x_type, y=y_type, c=c_type)

        # TODO assign label for y if y_id is None, as in that case the y-field will be missing from the response
        label_message = PlotDataFeatureLabels(x=x_id, y=y_id, c=c_id)

        # TODO Refactor pairwise call to separate function
        # Include pairwise results
        input_vectors = [PairwiseInputVector(x_id, x_type, x_vec)]
        if c_id is not None:
            input_vectors.append(PairwiseInputVector(c_id, c_type, c_vec))
        if y_id is not None:
            input_vectors.append(PairwiseInputVector(y_id, y_type, y_vec))


        pairwise_result = None

        if len(input_vectors) > 1:
            pairwise_result = self.get_pairwise_result(input_vectors)

        if pairwise_result is None:
            logger.warn("[WARNING] Pairwise results not included in returned object")

        return PlotDataResponse(types=type_message, labels=label_message, items=items,
                                cohort_set=cohort_info_obj_array,
                                counts=count_message, pairwise_result=pairwise_result, xUnits=units['x'], yUnits=units['y'])

    def get_feature_id_validity_for_array(self, feature_id_array):
        """
        For each feature identifier in an array, check whether or not the identifier is
        valid.

        Args:
            feature_id_array:

        Returns:
            Array of tuples - (feature identifier, <is valid>)
        """
        result = []
        for feature_id in feature_id_array:
            result.append((feature_id, is_valid_feature_identifier(feature_id)))

        return result

    @endpoints_method(PlotDataRequest, PlotDataResponse,
                      path='feature_data_plot', http_method='GET', name='feature_access.getFeatureDataForPlot')
    def data_access_for_plot(self, request):
        """ Used by the web application."""
        try:
            x_id = request.x_id
            y_id = request.y_id
            c_id = request.c_id
            logTransform = json.loads(request.log_transform)
            cohort_id_array = request.cohort_id

            # Check that all requested feature identifiers are valid. Do not check for y_id if it is not
            # supplied in the request.
            feature_ids_to_check = [x_id]
            if c_id is not None:
                feature_ids_to_check.append(c_id)
            if y_id is not None:
                feature_ids_to_check.append(y_id)

            valid_features = self.get_feature_id_validity_for_array(feature_ids_to_check)

            for feature_id, is_valid in valid_features:
                logging.info((feature_id, is_valid))
                if not is_valid:
                    logging.error("Invalid internal feature ID '{}'".format(feature_id))
                    raise NotFoundException()

            # Get the project IDs these cohorts' samples come from
            cohort_vals = ()
            cohort_params = ""

            for cohort in cohort_id_array:
                cohort_params += "%s,"
                cohort_vals += (cohort,)

            cohort_params = cohort_params[:-1]

            db = sql_connection()
            cursor = db.cursor()

            tcga_studies = fetch_isbcgc_project_set()

            cursor.execute("SELECT DISTINCT project_id FROM cohorts_samples WHERE cohort_id IN ("+cohort_params+");",cohort_vals)

            # Only samples whose source studies are TCGA studies, or extended from them, should be used
            confirmed_study_ids = []
            unconfirmed_study_ids = []

            for row in cursor.fetchall():
                if row[0] in tcga_studies:
                    if row[0] not in confirmed_study_ids:
                        confirmed_study_ids.append(row[0])
                elif row[0] not in unconfirmed_study_ids:
                    unconfirmed_study_ids.append(row[0])

            if len(unconfirmed_study_ids) > 0:
                projects = Project.objects.filter(id__in=unconfirmed_study_ids)

                for project in projects:
                    if project.get_my_root_and_depth()['root'] in tcga_studies:
                        confirmed_study_ids.append(project.id)

            return self.get_merged_feature_vectors(x_id, y_id, c_id, cohort_id_array, logTransform, confirmed_study_ids)
        except NotFoundException as nfe:
            # Pass through NotFoundException so that it is not handled as Exception below.
            raise nfe
        except Exception as e:
            logger.exception(e)
            raise InternalServerErrorException()

