Zeus - Agent Based Vulnerability Assessment
===========

Prerequisites
------------
```bash
sudo apt update
sudo apt-get install python3.6
sudo apt install python-pip 
``` 

Quick setup
------------
### 1. Clone repository
```bash
git clone https://github.com/RicardoAJPinto/Back-End-ProjectoFinal.git
cd Back-End-ProjectoFinal
``` 

### 2. Create database
```bash
python
from app import db
db.create_all()
exit()
``` 

### 3. Activate enviroment && install requirements
```bash
cd env/Scripts/
source activate
#--- Case you are on Windows:--------------
pip install -r requirements.txt
#---On unix system we advice to install:---
pip install -r requirementsLinux.txt
``` 

### 4. Finnaly, run the god damn project
```bash
python app.py
``` 

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
