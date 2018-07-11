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
from protorpc import remote, messages

from api_3.isb_cgc_api.isb_cgc_api_helpers import ISB_CGC_Endpoints

from api_3.api_helpers import sql_connection


@ISB_CGC_Endpoints.api_class(resource_name='files')
class FilesGetPath(remote.Service):
    GET_RESOURCE = endpoints.ResourceContainer(file_uuids=messages.StringField(1, repeated=True))

    class FilePaths(messages.Message):
        paths = messages.StringField(1, repeated=True)

    @endpoints.method(GET_RESOURCE, FilePaths, http_method='GET', path='file_paths')
    def get(self, request):
        """
        from the list of file gdc UUIDs, returns the google cloud storage file paths for those UUIDs.  the returned 
        filepaths will be in the same order as the passed in UUIDs
        """
        uuids = request.get_assigned_value('file_uuids')
        in_clause = ''
        params = []
        for uuid in uuids:
            in_clause += '%s, '
            params += ['{}'.format(uuid)]
        in_clause = in_clause[:-2]
        
        uuid2paths = {}
        sql = 'select file_gdc_id, file_name_key from {}_metadata_data_{} where file_gdc_id in ({}) order by 1, 2'
        programs = ['CCLE', 'TARGET', 'TCGA']
        db = sql_connection()
        for program in programs:
            if 'CCLE' == program:
                builds = ['HG19']
            else:
                builds = ['HG19', 'HG38']
            
            for build in builds:
                try:
                    cursor = db.cursor()
                    cursor.execute(sql.format(program, build, in_clause), params)
                    for row in cursor:
                        paths = uuid2paths.setdefault(row[0], [])
                        paths += [row[1]]
                except Exception as e:
                    print 'problem executing sql({}):\n\t{}\n\t{}'.format(e, sql, params)
                    raise
        filepaths = FilesGetPath.FilePaths()
        filepaths.paths = [item for sublist in uuid2paths.values() for item in sublist]
        return filepaths
