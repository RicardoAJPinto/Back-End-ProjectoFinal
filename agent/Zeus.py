#!/usr/bin/python
import schedule
import time
import uuid
import rsa
import base64
import requests 
import sys
import json

with open('public.pem', mode='rb') as pubfile:
  keydata = pubfile.read()
  pub_key = rsa.PublicKey.load_pkcs1(keydata)
with open('api.pem', mode='rb') as idfile:
  api_file = idfile.read()

from config import headers
# Url of the endpoint to post the scans
url = 'http://127.0.0.1:5000/api/scans'
# url = 'https://zeus-security.herokuapp.com/api/scans'

machine_id=hex(uuid.getnode()).encode('utf8')
encrypted = rsa.encrypt(machine_id, pub_key)
base64_machine = image_string = base64.b64encode(encrypted)

headers["machine-id"] = base64_machine
print(headers)
headers["user-id"] = api_file
print(headers)

from DetectOS import *
requestpost = requests.post(url , json=payload, headers=headers)
print(requestpost)

print("Done +1 post")

# schedule.every(1).minute.do(scan)
# # schedule.every().hour.do(scan)
# # schedule.every().day.at("10:30").do(scan)

# while True:
#     schedule.run_pending()
    
