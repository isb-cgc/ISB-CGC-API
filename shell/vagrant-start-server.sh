export $(cat /home/vagrant/parentDir/secure_files/.env | grep -v ^# | xargs) 2> /dev/null
