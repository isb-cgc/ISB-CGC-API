###
# Copyright 2015-2025, Institute for Systems Biology
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

#!/bin/bash -eo pipefail

if [ -n "$CI" ]; then
    echo "Check our Python and Ubuntu versions since they keep getting updated without warning..."

    ls -l /usr/bin/python3*
    cat /etc/os-release

    export HOME=/home/circleci/${CIRCLE_PROJECT_REPONAME}
    export HOMEROOT=/home/circleci/${CIRCLE_PROJECT_REPONAME}
else
    if ( "/home/vagrant/API/shell/get_env.sh" ) ; then
        export $(cat ${ENV_FILE_PATH} | grep -v ^# | xargs) 2> /dev/null
        # Confirm some relevant values to ensure we found a valid .env
        if [ -z "${SECURE_LOCAL_PATH}" ] || [ "${SECURE_LOCAL_PATH}" == "" ] ; then
            echo "[ERROR] SECURE_LOCAL_PATH not found, but this is a VM build! Something might be wrong with your .env file"
            echo "or your secure_files directory."
            exit 1
        fi
    else
        exit 1
    fi
    export HOME=/home/vagrant
    export HOMEROOT=/home/vagrant/API
fi

export DEBIAN_FRONTEND=noninteractive

# Remove .pyc files; these can sometimes stick around and if a
# model has changed names it will cause various load failures
find . -type f -name '*.pyc' -delete

echo "Updating packing lists..."
apt-get update -qq

# Install and update apt-get info
echo "Preparing System"
apt-get -y --force-yes install software-properties-common ca-certificates gnupg

# Install apt-get dependencies
echo "Installing Dependencies..."
apt-get install -y --force-yes unzip libffi-dev libssl-dev git g++ curl dos2unix pkg-config
apt-get install -y --force-yes python3-distutils libpython3-dev build-essential
apt-get install -y --force-yes python3-pip

echo "Dependencies Installed"

# If this is local development, clean out lib for a re-structuring
if [ -z "${CI}" ]; then
    # Clean out lib to prevent confusion over multiple builds in local development
    # and prep for local install
    echo "Emptying out ${HOMEROOT}/lib/ ..."
    rm -rf "${HOMEROOT}/lib/"
    echo "Confirming clearance of lib:"
    ls ${HOMEROOT}/lib/
fi

# Install PIP + Dependencies
echo "Installing pip3..."
curl --silent https://bootstrap.pypa.io/get-pip.py | python3

# Install our primary python libraries
# If we're not on CircleCI, or we are but the lib directory isn't there (cache miss), install lib
if [ -z "${CI}" ] || [ ! -d "lib" ]; then
    echo "Installing Python Libraries..."
    pip install -r ${HOMEROOT}/requirements.txt -t ${HOMEROOT}/lib
else
    echo "Using restored cache for Python Libraries"
fi

# Install Google Cloud SDK
# If we're not on CircleCI or we are but google-cloud-sdk isn't there, install it
if [ -z "${CI}" ] || [ ! -d "/usr/lib/google-cloud-sdk" ]; then
    echo "Installing Google Cloud SDK..."
    export CLOUDSDK_CORE_DISABLE_PROMPTS=1
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
    apt-get -y install apt-transport-https ca-certificates
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
    apt-get update -qq
    apt-get -y install google-cloud-sdk
    apt-get -y install google-cloud-sdk-app-engine-python
    echo "Google Cloud SDK Installed"
fi
