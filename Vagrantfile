# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/xenial64"

  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 8484, host: 8484
  config.vm.network "forwarded_port", guest: 5432, host: 5432

  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 2
  end

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  config.vm.synced_folder ".", "/vagrant_data"

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get upgrade -y
    sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common vim git python-pip build-essential libbz2-dev zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev ntp
    sudo systemctl enable ntp
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get -y install docker-ce docker-ce-cli containerd.io
    wget https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tgz
    tar -xvf Python-3.7.6.tgz
    rm -rf Python-3.7.6.tgz
    cd Python-3.7.6
    ./configure
    make -j 1
    sudo make altinstall
    cd ..
    rm -rf Python-3.7.6
    sudo pip3.7 install --upgrade pip
    sudo pip3.7 install docker-compose
    cd /vagrant_data
    sudo pip3.7 install -r requirements.txt
  SHELL
end
