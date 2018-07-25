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

points = 0
# Url of the endpoint to post the scans
url = 'https://zeus-sec.herokuapp.com/api/scans'
url_reload = 'https://zeus-sec.herokuapp.com/reload'

#url = 'http://127.0.0.1:5000/api/scans'
#url_reload = 'http://127.0.0.1:5000/reload' 

machine_id=hex(uuid.getnode()).encode('utf8')
encrypted = rsa.encrypt(machine_id, pub_key)

base64_machine = base64.b64encode(encrypted)
headers = {}
headers["machine-id"] = base64_machine
headers["user-id"] = api_file

# def scan():  
payload_zeus = {}
request = requests.get(url_reload, headers=headers)#.json()
result_scans = request.json()

if result_scans["DetectOS:"] == True:
  import DetectOS
  result = DetectOS.OperatingSystem(payload_zeus)
  print(result)
  
  if result["lsass"] == "Activated":
    points = points + 10
  if result["antivirus"] != None:
    points = points + 10
  if result_scans["NewScan:"] == False:
    result["points"] = points
    requestpost = requests.post(url, json=result, headers=headers)
    print("DetectOS has been executed sucessfully!")
    print(result)

# Scann added
if result_scans["NewScan:"] == True:
  import NewScan
  result1 = NewScan.runscan(result)
  if result1["system"] != '':
    points = points + 5
    result1["points"] = points
  print(result1)
  requestpost = requests.post(url , json=result1, headers=headers)
  print("The inserted scan has been executed sucessfully!")

