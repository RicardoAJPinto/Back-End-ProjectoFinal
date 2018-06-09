SHELL = /bin/bash
WORKDIR = /vagrant

PSQL = sudo -u postgres psql
DBNAME = projetofinal_dev
DBUSER = dev_user
DBPASS = dev_pass

db/console:
	$(PSQL) $(DBNAME)

db/create: db/create/user db/create/database

db/destroy: db/destroy/database db/destroy/user

db/create/database:
	@echo "--> create DB"
	$(PSQL) -c "CREATE DATABASE $(DBNAME) OWNER $(DBUSER);"

db/create/user:
	@echo "--> create DB user"
	$(PSQL) -c "CREATE USER $(DBUSER) WITH PASSWORD '$(DBPASS)';"

db/create/tables:
	python -c 'from app import db;db.create_all();'

db/destroy/database:
	@echo "--> drop DB"
	$(PSQL) -c "DROP DATABASE IF EXISTS $(DBNAME);"

db/destroy/user:
	@echo "--> delete DB user"
	$(PSQL) -c "DROP USER IF EXISTS $(DBUSER);"

flask/server:
	python app.py
