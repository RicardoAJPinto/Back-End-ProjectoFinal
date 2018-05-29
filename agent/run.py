import os
import json
import requests
import subprocess
import uuid
from powershell import *
from DetectOS import *

agent = Flask(__name__)
agent.config.from_pyfile('confg.py')

r = requests.post('http://127.0.0.1:5000/connection', json=dataFn)