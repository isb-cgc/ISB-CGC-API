# -*- mode: ruby -*-
# vi: set ft=ruby :
ENV["VAGRANT_DISABLE_STRICT_DEPENDENCY_ENFORCEMENT"] = "1"

Vagrant.configure(2) do |config|

  config.vm.provider "virtualbox" do |vb|
     # Display the VirtualBox GUI when booting the machine
     # vb.gui = true

     # Customize the amount of memory on the VM:
     vb.memory = "4096"

     vb.customize ["modifyvm", :id, "--uart1", "0x3F8", "4"]
     vb.customize ["modifyvm", :id, "--uartmode1", "file", File::NULL]

     vb.customize ["modifyvm", :id, "--nestedpaging", "off"]
     vb.customize ["modifyvm", :id, "--cpus", 2]
     vb.customize ["modifyvm", :id, "--paravirtprovider", "default"]
   end

  config.vm.box = "debian/bookworm64"
  config.vm.box_version = "12.20250126.1"

  # API ports
  config.vm.network "forwarded_port", guest: 8095, host: 8095
  config.vm.network "forwarded_port", guest: 9010, host: 9010
  config.vm.network "forwarded_port", guest: 22, host: 2300, id: "ssh"

  config.vm.synced_folder ".", "/home/vagrant/API"
  config.vm.synced_folder "../", "/home/vagrant/parentDir"
  config.vm.synced_folder "../secure_files", "/home/vagrant/secure_files"

  # Map Common and lib for API
  config.vm.synced_folder "../ISB-CGC-Common", "/home/vagrant/API/ISB-CGC-Common"

  # To avoid issues with scripts getting Windows line terminators, always install dos2unix and convert the
  # shell directory before the rest of the provisioning scripts run
  config.vm.provision :shell, inline: "sudo apt-get update", :run => 'always'
  config.vm.provision :shell, inline: "sudo apt-get install dos2unix", :run => 'always'
  config.vm.provision :shell, inline: "dos2unix /home/vagrant/API/shell/*.sh", :run => 'always'
  config.vm.provision :shell, inline: "echo 'source /home/vagrant/API/shell/env.sh' > /etc/profile.d/sa-environment.sh", :run => 'always'
  config.vm.provision "shell", path: 'shell/install-deps.sh'
  config.vm.provision "shell", path: 'shell/create-database.sh'
  config.vm.provision "shell", path: 'shell/database-setup.sh'
  config.vm.provision "shell", path: 'shell/vagrant-start-server.sh', :run => 'always'
  config.vm.provision "shell", path: 'shell/vagrant-set-env.sh', :run => 'always'
end