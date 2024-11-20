#!/bin/bash
echo 'export PYTHONPATH=/home/vagrant/API:/home/vagrant/API/lib:/home/vagrant/API/IDC-Common' | tee -a /home/vagrant/.bash_profile
echo 'export SECURE_LOCAL_PATH=../parentDir/secure_files/idc/' | tee -a /home/vagrant/.bash_profile
echo 'export DJANGO_SETTINGS_MODULE=settings' | tee -a /home/vagrant/.bash_profile
echo 'export FLASK_APP=api'
echo 'export FLASK_RUN_PORT=8095'
echo 'export FLASK_DEBUG=1'
source /home/vagrant/.bash_profile

chmod +x /home/vagrant/API/shell/python-su.sh