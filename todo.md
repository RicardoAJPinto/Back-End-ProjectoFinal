
# Projeto final - BOSS 1

# New things to do:
* Colocar issues no github + resolver quando conseguirmos
* Polir ultimas coisas que adicionamos e ver se não há mais bugs ou coisas a resolver(add to trello)

# Bugs to solve:
* ID of tests are the same for all the users
* Update campo do crontab e testar numa maquina
* Comandos do quickstart mudar para python3
* daemon vs crontab?

# Features to add:

* ## Docker com Zeus já instalado
Isto pode ser uma versão que as pessoas podem utilizar para as máquinas antes de implementarmos as websockets

* ## Websocket 
Transferencia do agente a partir de m�quinas que nao contenham GUI para poder aceder ao website

* ## Criação de alertas
Exemplo: Quando a percentagem de cpu for maior a 70% enviar email 

* ## Continuous Integration
Upgrade TravisCI file + Testar criação autónoma da DB

* ## Ver quais a vulnerabilidades do computador e seu risco associado
Checkar vulneberabiblidades com uma API que contém todas as vulnerabilidades de um sistema(https://www.circl.lu/services/cve-search/ )

* ## Coveralls

# Detalhes a discutir:
* Encriptar ou colocar apenas binários do ficheiro zeus que comunica com o servidor (Para não haver malta a fingir que efetua uma análise à máquina e envia os dados corretos em json para o servidor)

# Projeto final - BOSS isto está a ficar abusado

### Books to help:
Python Microservices Development.pdf

## Monitorização de serviços
Sections to check: 
* Centralizing logs
* Performance metrics

Package to check:
* logging package
* Graylog ( need docker installed)

## Tests
Ver livro: Python Microservices Development
* Unit tests: Make sure a class or a function works as expected in isolation
* Functional tests: Tests that interact with the published API by sending HTTP requests and asserting the HTTP responses.
* Integration tests: Verify how a microservice integrates with all its network
dependencies
* Load tests: Measure the microservice performances
* End-to-end tests: Verify that the whole system works with an end-to-end test


To run repetitive background tasks in Python
web apps is to use Celery (http://docs.celeryproject.org), a distributed task queue that
can execute some work in a standalone process.

## Developer documentation 
* To use Sphinx
* Swagger using Open API 2.0 specification


## Improve perfomance
* check celery + redis
* Cache pages
* Compression  to reduce size of data transfers and speed up processing
* or binary payloads - JUST IF DEALS A LOT OF DATA
* processos assincronos(acho que nao preciso de preocupador pkausa de devops area)


## Checkar boa concurrencia após ter os basicos do projeto:
Graylog
Duosadadasdax(empresa comprada por 2.5mil milhoes)
