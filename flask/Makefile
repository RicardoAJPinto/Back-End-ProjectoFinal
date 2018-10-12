SHELL = /bin/bash
WORKDIR = /vagrant/flask

PSQL = sudo -u postgres psql
DBNAME = projetofinal_dev
DBUSER = dev_user
DBPASS = dev_pass

db/console:
	$(PSQL) $(DBNAME)

db/create: db/create/user db/create/database db/install/uuid  

db/destroy: db/destroy/database db/destroy/user

db/create/tables:
	@echo "--> create DB tables using SQAlchemy"
	pipenv run python -c 'from app import db; db.create_all();'
	@echo "--> testing db creation"
	$(PSQL) -d $(DBNAME) -c "\dt"
	# Creates test sample
	@echo "--> Create test sample"
	$(PSQL) -d $(DBNAME) -c "INSERT INTO test VALUES (1, True, False);"
	@echo "--> testing test set basic creation"
	$(PSQL) -d $(DBNAME) -c "SELECT * FROM test;"
	# Creates admin account
	# @echo "--> Create admin user"
    # $(PSQL) -d $(DBNAME) -c "INSERT INTO "user" (id, email, password, active) VALUES (99, 'admin@zeus.pt', 'zeuspowerADMIN', True);"
    # @echo "--> create role for admin"
    # $(PSQL) -d $(DBNAME) -c "INSERT INTO role (id, name) VALUES (99, 'admin');"
    # @echo "--> create relationship role for admin"
    # $(PSQL) -d $(DBNAME) -c "INSERT INTO roles_users (user_id, role_id) VALUES (99, 99);"

# Creates a image to represent the ER Diagram
db/create/er:
	@echo "--> create ER Diagram from DB using ERAlchemy"
	pipenv run eralchemy -i postgresql://$(DBUSER):$(DBPASS)@localhost/$(DBNAME) -o ER.png

############
### db/create
############
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


############
### db/destroy
############
db/destroy/database:
	@echo "--> drop DB"
	$(PSQL) -c "DROP DATABASE IF EXISTS $(DBNAME);"

db/destroy/user:
	@echo "--> delete DB user"
	$(PSQL) -c "DROP USER IF EXISTS $(DBUSER);"

flask/dev:
	FLASK_ENV=development python app.py

flask/prod:
	FLASK_ENV=production python app.py

	