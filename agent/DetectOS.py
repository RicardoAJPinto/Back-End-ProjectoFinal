#!/usr/bin/python
#Every plataform
from platform import linux_distribution, uname
import sys
import json 

def OperatingSystem():
  payload_zeus = {}
  if linux_distribution()[1] == ' ':
    payload_zeus["Public Release:"] = linux_distribution()[1]
  for i in range(0, len(uname())):
    payload_zeus[uname()._fields[i]] = uname()[i]
  return payload_zeus

  
