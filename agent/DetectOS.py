#!/usr/bin/python
#Every plataform
from platform import linux_distribution, uname
import sys
import json 
import requests 
import uuid
import rsa
import base64

with open('public.pem', mode='rb') as pubfile:
  keydata = pubfile.read()
  pub_key = rsa.PublicKey.load_pkcs1(keydata)
with open('api.pem', mode='rb') as idfile:
  api_file = idfile.read()

def OperatingSystem():
  payload = {}
  if linux_distribution()[1] == ' ':
    payload["Public Release:"] = linux_distribution()[1]
  for i in range(0, len(uname())):
    payload[uname()._fields[i]] = uname()[i]
  print(payload)

  from config import headers
  # Url of the endpoint to post the scans
  url = 'http://127.0.0.1:5000/api/scans'
  
  machine_id=hex(uuid.getnode()).encode('utf8')
  encrypted = rsa.encrypt(machine_id, pub_key)

  base64_machine = image_string = base64.b64encode(encrypted)

  headers["machine-id"] = base64_machine
  print(headers)
  headers["user-id"] = api_file
  print(headers)

  requestpost = requests.post(url , json=payload, headers=headers)
  print(requestpost)

  
