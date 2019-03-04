# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure(2) do |config|
    config.vm.box_url = "https://app.vagrantup.com/ubuntu/boxes/xenial64"
    config.vm.box = "ubuntu/xenial64"

    # API ports
    config.vm.network "forwarded_port", guest: 8090, host: 8090
    config.vm.network "forwarded_port", guest: 9000, host: 9000

    config.vm.synced_folder ".", "/home/vagrant/API"
    config.vm.synced_folder "../", "/home/vagrant/parentDir"

    # Map Common and lib for API
    config.vm.synced_folder "../ISB-CGC-Common", "/home/vagrant/API/ISB-CGC-Common"

    config.vm.provision "shell", path: 'shell/install-deps.sh'
    config.vm.provision "shell", path: 'shell/vagrant-start-server.sh'
    config.vm.provision "shell", path: 'shell/vagrant-set-env.sh'
end