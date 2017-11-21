if [ -n "$CI" ]; then
    export HOME=/home/ubuntu/${CIRCLE_PROJECT_REPONAME}
    export HOMEROOT=/home/ubuntu/${CIRCLE_PROJECT_REPONAME}

# Clone dependencies
    git clone -b isb-cgc-prod https://github.com/isb-cgc/ISB-CGC-Common.git

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
    add-apt-repository -y ppa:fkrull/deadsnakes-python2.7
    apt-get update -qq
    apt-get install -qq -y python2.7
fi

# Install apt-get dependencies
echo "Installing Dependencies..."
apt-get install -qq -y unzip libffi-dev libssl-dev libmysqlclient-dev python2.7-dev git
echo "Dependencies Installed"

# Install PIP + Dependencies
echo "Installing Python Libraries..."
curl --silent https://bootstrap.pypa.io/get-pip.py | python
# If we are in Frameworks 2.0, uncomment this and remove the endpoints entry from the libraries: section in the app.yaml
# pip install -t lib google-endpoints --ignore-installed --upgrade
pip install -q -r ${HOMEROOT}/requirements.txt -t ${HOMEROOT}/lib --upgrade --only-binary all
echo "Libraries Installed"

# Install Google App Engine
echo "Installing Google App Engine..."
wget -q https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.61.zip -O ${HOME}/google_appengine.zip
unzip -nq ${HOME}/google_appengine.zip -d $HOME
export PATH=$PATH:${HOME}/google_appengine/
export PYTHONPATH=$PYTHONPATH:${HOME}/google_appengine/
echo $PYTHONPATH
echo "Google App Engine Installed"

# Install Google Cloud SDK
echo "Installing Google Cloud SDK..."
export CLOUDSDK_CORE_DISABLE_PROMPTS=1
curl https://sdk.cloud.google.com | bash
export PATH=$PATH:${HOME}/google-cloud-sdk/bin
echo 'export PATH=$PATH:${HOME}/google-cloud-sdk/bin' | tee -a ${HOME}/.bash_profile
echo "Google Cloud SDK Installed"
