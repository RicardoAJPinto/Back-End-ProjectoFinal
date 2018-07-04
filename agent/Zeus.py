#!/usr/bin/python
import schedule
import time
import uuid
import rsa
import base64
import requests 
import sys
import json
import DetectOS


with open('public.pem', mode='rb') as pubfile:
  keydata = pubfile.read()
  pub_key = rsa.PublicKey.load_pkcs1(keydata)
with open('api.pem', mode='rb') as idfile:
  api_file = idfile.read()

from config import headers
# Url of the endpoint to post the scans
url = 'http://127.0.0.1:5000/api/scans'
url_reload = 'http://127.0.0.1:5000/reload'
  
machine_id=hex(uuid.getnode()).encode('utf8')
encrypted = rsa.encrypt(machine_id, pub_key)

base64_machine = image_string = base64.b64encode(encrypted)

headers["machine-id"] = base64_machine
headers["user-id"] = api_file

# def scan():  
request = requests.get(url_reload, headers=headers)#.json()
result_scans = request.json()

if result_scans["DetectOS:"] == True:
  result = DetectOS.OperatingSystem()
  requestpost = requests.post(url , json=result, headers=headers)
print("Done +1 post")
