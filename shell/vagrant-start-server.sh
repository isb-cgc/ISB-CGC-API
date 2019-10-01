export $(cat /home/vagrant/parentDir/secure_files/idc/.env | grep -v ^# | xargs) 2> /dev/null
