Zeus - Agent Based Vulnerability Assessment
===========

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
# 7. Go to /vagrant folder
cd /vagrant
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
Change files(path to API or DB):
* Dashboard.py
* config.cfg
* app.py

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/RicardoAJPinto/Back-End-ProjectoFinal)
Used technologies
------------
* Python 3.6.4
* Pip 
* Flask
* PostgreSQL + SQLAlchemy
* (to be used: Vue.js)

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
