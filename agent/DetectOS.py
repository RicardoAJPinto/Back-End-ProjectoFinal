#!/usr/bin/python
#Every plataform
from platform import linux_distribution, uname
import sys
import json 
import requests 

payload = {}
if linux_distribution()[1] == ' ':
	payload["Public Release:"] = linux_distribution()[1]
for i in range(0, len(uname())):
  payload[uname()._fields[i]] = uname()[i]
print(payload)
# url = 'http://127.0.0.1:5000/api/scans'
# requestpost = requests.post(url , json=payload)
# print(requestpost)
