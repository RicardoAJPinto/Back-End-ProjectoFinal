[![Build Status](https://travis-ci.org/RicardoAJPinto/Back-End-ProjectoFinal.svg?branch=master)](https://travis-ci.org/RicardoAJPinto/Back-End-ProjectoFinal)
[![Known Vulnerabilities](https://snyk.io/test/github/RicardoAJPinto/Back-End-ProjectoFinal/badge.svg)](https://snyk.io/test/github/RicardoAJPinto/Back-End-ProjectoFinal)
[![Heroku](https://heroku-badge.herokuapp.com/?app=zeus-sec)](http://zeus-sec.herokuapp.com)

Zeus - Agent Based Vulnerability Assessment
===========
![logo do ipt](http://portal2.ipt.pt/img/logo.png "Instituto Politécnico de Tomar")

The present project was elaborated within the scope of the final project discipline.

The objective of this project is to develop and make available a system to monitor a set of machines and services, capable of summarizing information at a central point, available through the web interface. This should provide information about possible vulnerabilities, generate reports of the analyzes made and possibly possible solutions to the problems encountered.

For this user will have available in the web application a cross-platform agent. This agent must be installed on the target machines, being responsible for running tests in the defined time intervals and communicating results to the server


Website:  https://zeus-sec.herokuapp.com/ 

Prerequisites
------------
#### 1. Install(lastest versions) :
* VirtualBox
* Vagrant 
* Git Bash

Deploy project on Vagrant 
------------
```bash
# 2. Open a git bash shell
# 3. Clone the repo
git clone https://github.com/RicardoAJPinto/Back-End-ProjectoFinal.git
# 4. Go to the project folder
cd Back-End-ProjectoFinal
# 5. Download and provision the development VM (takes some minutes)
vagrant up
# The development VM is now ready, everything has been installed
# 6. SSH into the VM
vagrant ssh
# The /vagrant folder is shared between host and guest VM and contains the project files
# 7. Go to /vagrant/flask folder where makefile is located
cd /vagrant/flask
# 8. Start the virtual environment using Pipenv
pipenv shell
# 9. Start the server with one of the following
make flask/dev
make flask/prod
python app.py
# 10. In the host open http://localhost:5000

# 11. When finish, exit the guest and don't forget to halt the VM
vagrant halt # in the host

# Other relevant commands
pipenv install --dev
pipenv install / uninstall <module>
make <see Makefile file>
``` 

Connect to DB 
------------
```bash
sudo -u postgres psql postgres
\l #show all database to connect
\connect database_name
SELECT * FROM table_name;
\q #Exit
``` 

Deploy project on Heroku
------------

#### 1. Install :
* Heroku CLI
* Git Bash

#### 2. Change files(path to API or DB):
* Dashboard.py
* config.cfg
* agent/Detect.OS.py

#### 3. Simple commands to iteract with Heroku :
```bash
heroku login
heroku pg:psql #Connect to PostgreSQL
heroku run bash #That's it xD 
``` 

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/RicardoAJPinto/Back-End-ProjectoFinal)

If you need help: https://devcenter.heroku.com/articles/getting-started-with-python#deploy-the-app 

Used technologies
------------
* Python 3.6.4
* Pip 
* Flask
* PostgreSQL + SQLAlchemy

Project overview
------------
```
|   AdminPage.py 	<- Flask-admin page
|   api.py		    <- API endpoints 
|   app.py		    <- Core of the app
|   config.py		  <- Configurations 
|   model.py		  <- Model
|   README.md		  <- Maybe what you're seeing
|   views.py		  <- Views 
|
+---agent 		    <- Location of all scripts
|   |   config.py	<- All the necessary configs to the main script
|   |   DetectOS.py	<- Scan to get information from the machine( more here: https://github.com/mrsequeira/Scripts)
|   |   Zeus.py		<- Main script
|        
+---env
|   (....)
|
+---templates 		<- Location of all the "beauty"
|   (........)
|   |   
|   +---admin
|   |       index.html
|   |       
|   +---layouts
|   |       layout1.html <- Base for the HomePage views
|   |       layout2.html <- Base for the Dashboard views
|   |       
|   \---security	 <- Location of all the "beauty"
|   | 	(......)
```

Bugs and Issues
------------

Have a bug or an issue with this template? [Open a new issue](https://github.com/RicardoAJPinto/Back-End-ProjectoFinal/issues) here on GitHub.
