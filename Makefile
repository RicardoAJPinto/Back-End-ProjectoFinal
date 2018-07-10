SHELL = /bin/bash
WORKDIR = /vagrant/flask

PSQL = sudo -u postgres psql
DBNAME = projetofinal_dev
DBUSER = dev_user
DBPASS = dev_pass

db/console:
	$(PSQL) $(DBNAME)

db/create: /db/create/tables db/create/user db/create/database db/install/uuid db/create/test

db/destroy: db/destroy/database db/destroy/user

db/install/uuid:
	@echo "--> install DB extension to have uuid_generate_v4()"
	$(PSQL) -d $(DBNAME) -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
	@echo "--> testing postgreSQL uuid_generate_v4() function"
	$(PSQL) -d $(DBNAME) -c "SELECT uuid_generate_v4();"

db/create/database:
	@echo "--> create DB"
	$(PSQL) -c "CREATE DATABASE $(DBNAME) OWNER $(DBUSER);"

db/create/user:
	@echo "--> create DB user"
	$(PSQL) -c "CREATE USER $(DBUSER) WITH PASSWORD '$(DBPASS)';"

db/destroy/database:
	@echo "--> drop DB"
	$(PSQL) -c "DROP DATABASE IF EXISTS $(DBNAME);"

db/destroy/user:
	@echo "--> delete DB user"
	$(PSQL) -c "DROP USER IF EXISTS $(DBUSER);"

db/create/test:
	@echo "--> Create test sample"
	$(PSQL) -d $(DBNAME) -c "INSERT INTO test VALUES (1, True, False);"

db/create/tables:
	@echo "--> create DB tables using SQAlchemy"
	$(shell cd $(WORKDIR); pipenv run python -c 'from app import db; db.create_all();'	) 
	

db/create/er:
	@echo "--> create ER Diagram from DB using ERAlchemy"
	pipenv run eralchemy -i postgresql://$(DBUSER):$(DBPASS)@localhost/$(DBNAME) -o ER.png

flask/dev:
	FLASK_ENV=development python flask/app.py

flask/prod:
	FLASK_ENV=production python flask/app.py

	