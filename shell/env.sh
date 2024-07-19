###
# Copyright 2015-2024, Institute for Systems Biology
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
# Location of the .env file
# This is NOT a relative path and should NOT be the same value as SECURE_LOCAL_PATH
# This should be an absolute path on the VM.
# The default value assumes a SECURE_LOCAL_PATH setting of ../parenDir/secure_files/
if [ ! -f "/home/vagrant/API/secure_path.env" ]; then
    echo "No secure_path.env found - using default value of /home/vagrant/secure_files/.env."
    echo "If your .env is not at this location, you must make a secure_path.env file with the SECURE_LOCAL_PATH"
    echo "value as its only entry and place it in the root directory (/home/vagrant/www)."
    export ENV_FILE_PATH=/home/vagrant/secure_files/.env
else
    echo "secure_path.env setting found."
    export ENV_FILE_PATH=$(cat /home/vagrant/API/secure_path.env)
    echo ".env file assumed to be found at ${ENV_FILE_PATH}"
fi
