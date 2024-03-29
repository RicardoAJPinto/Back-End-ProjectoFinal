# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  
  # o 16.04 é a versão em uso por muitos cloud providers
  config.vm.box = "bento/ubuntu-16.04" 
  config.vm.box_check_update = true

  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.vm.provider "virtualbox" do |vb|
    vb.linked_clone = true
    vb.memory = "1024"
    vb.cpus = 1
  end

  config.vm.provision "shell", inline: <<-SHELL
    export HOME=/home/vagrant
    sudo apt-get update -yq
    sudo apt-get install -yq ntp
    sudo apt-get install -yq git

    # install python3.6 (in Ubuntu 16.04)
    sudo apt-get install -yq software-properties-common
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt-get update -y
    sudo apt-get install -yq python3.6

    # install python dev libs and headers to build modules
    # sudo apt-get install -yq python-dev # do I need this?
    sudo apt-get install -yq python3.6-dev

    # install pip for python3.6
    su vagrant -c 'curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py'
    sudo python3.6 get-pip.py
    sudo -H pip install pip==18.0 # Avoided issue, problems with 18.1 version

    # nota: talvez tenha que mudar os nomes ao python, python3.5 e python3.6
    # install Pipenv (needed for Heroku, high-level virtualenv, ala Bundler)
    # su vagrant -c 'pip3 install --user pipenv'
    sudo pip install pipenv # install system wide
    
    # install postgres 
    sudo apt-get install -yq postgresql
    sudo apt-get install -yq libpq-dev
    
    # install graphviz for ER diagrams
    sudo apt-get install -yq graphviz libgraphviz-dev graphviz-dev pkg-config
    
    # install all the python modules in the virtual env,
    # activate the venv, create DB, USER, etc
    # create all the DB tables
    cd /vagrant/flask
    sudo -u vagrant -- bash -c 'pipenv install --dev'
    sudo -u vagrant -- bash -c 'make db/create'
    sudo -u vagrant -- bash -c 'pipenv run make db/create/tables'
    
    # pipenv is not found this way...
    # su vagrant -c 'pipenv install &&
    #              pipenv shell &&
    #               make db/create &&
    #               make db/create/tables'
  SHELL

  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  # Provision python development environment

  # config.vm.provision "shell", inline: <<-SHELL
  #   export HOME=/home/vagrant

  #   sudo apt-get update
  #   sudo apt-get install -yq ntp git python-dev python-virtualenv postgresql libpq-dev

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
end