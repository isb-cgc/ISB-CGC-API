if [ -n "$CI" ]; then
    export HOME=/home/circleci/${CIRCLE_PROJECT_REPONAME}
    export HOMEROOT=/home/circleci/${CIRCLE_PROJECT_REPONAME}
    # Clone dependencies
    git clone -b isb-cgc-test https://github.com/isb-cgc/ISB-CGC-Common.git
else
    export $(cat /home/vagrant/www/.env | grep -v ^# | xargs) 2> /dev/null
    export HOME=/home/vagrant
    export HOMEROOT=/home/vagrant/www
fi

# Install and update apt-get info
echo "Preparing System..."
apt-get -y install software-properties-common

if [ -n "$CI" ]; then
    # CI Takes care of Python update
    apt-get update -qq
else
    # Add apt-get repository to update python from 2.7.6 (default) to latest 2.7.x
    add-apt-repository -y ppa:jonathonf/python-2.7
    apt-get update -qq
    apt-get install -qq -y python2.7
fi

# Install apt-get dependencies
echo "Installing Dependencies..."
apt-get install -qq -y unzip libffi-dev libssl-dev mysql-client libmysqlclient-dev python2.7-dev git
echo "Dependencies Installed "

# Install PIP + Dependencies
echo "Installing PIP..."
curl --silent https://bootstrap.pypa.io/get-pip.py | python
echo "...PIP installed."

# Install our primary python libraries
# If we're not on CircleCI, or we are but the lib directory isn't there (cache miss), install lib
if [ -z "${CI}" ] || [ ! -d "lib" ]; then
    echo "Installing Python Libraries..."
    pip install -q -r ${HOMEROOT}/requirements.txt -t ${HOMEROOT}/lib --upgrade --only-binary all
else
    echo "Using restored cache for Python Libraries"
fi

# Install Google App Engine
# If we're not on CircleCI or we are but google_appengine isn't there, install it
if [ -z "${CI}" ] || [ ! -d "google_appengine" ]; then
    echo "Installing Google App Engine..."
    wget https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.69.zip -O ${HOME}/google_appengine.zip
    unzip -n -qq ${HOME}/google_appengine.zip -d $HOME
    export PATH=$PATH:${HOME}/google_appengine/
    echo "Google App Engine Installed"
else
    echo "Using restored cache for Google App Engine. "
fi

# Install Google Cloud SDK
# If we're not on CircleCI or we are but google-cloud-sdk isn't there, install it
if [ -z "${CI}" ] || [ ! -d "google-cloud-sdk" ]; then
    echo "Installing Google Cloud SDK..."
    export CLOUDSDK_CORE_DISABLE_PROMPTS=1
    curl https://sdk.cloud.google.com | bash
    export PATH=$PATH:${HOME}/google-cloud-sdk/bin
    echo 'export PATH=$PATH:${HOME}/google-cloud-sdk/bin' | tee -a ${HOME}/.bash_profile
    echo "Google Cloud SDK Installed"
else
    echo "Using restored cache for Google Cloud SDK."
fi

