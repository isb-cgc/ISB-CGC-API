###
# Copyright 2015-2023, Institute for Systems Biology
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
###

echo 'export PYTHONPATH=/home/vagrant/API:/home/vagrant/API/lib:/home/vagrant/API/apiv4:/home/vagrant/API/ISB-CGC-Common' | tee -a /home/vagrant/.bash_profile
echo 'export SECURE_LOCAL_PATH=../parentDir/secure_files/' | tee -a /home/vagrant/.bash_profile
echo 'export DJANGO_SETTINGS_MODULE=settings' | tee -a /home/vagrant/.bash_profile
chmod +x /home/vagrant/API/shell/python-su.sh
