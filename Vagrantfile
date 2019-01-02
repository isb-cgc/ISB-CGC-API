# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure(2) do |config|
    required_plugins = %w( vagrant-vbguest vagrant-disksize )
    _retry = false
    required_plugins.each do |plugin|
        unless Vagrant.has_plugin? plugin
            system "vagrant plugin install #{plugin}"
            _retry=true
        end
    end

    if (_retry)
        exec "vagrant " + ARGV.join(' ')
    end

    config.vm.box_url = "https://app.vagrantup.com/debian/boxes/stretch64"
    config.vm.box = "debian/stretch64"
    config.disksize.size = "40GB"

    # API ports
    config.vm.network "forwarded_port", guest: 8090, host: 8090
    config.vm.network "forwarded_port", guest: 9000, host: 9000

    config.vm.synced_folder ".", "/home/vagrant/API"
    config.vm.synced_folder "../", "/home/vagrant/parentDir"

    # Map Common and lib for API
    config.vm.synced_folder "../ISB-CGC-Common", "/home/vagrant/API/ISB-CGC-Common"
    config.vm.synced_folder "../secure_files", "/home/vagrant/API/secure_files"

    config.vm.provision "shell", path: 'shell/install-deps.sh'
    config.vm.provision "shell", path: 'shell/vagrant-start-server.sh'
    config.vm.provision "shell", path: 'shell/vagrant-set-env.sh'
end