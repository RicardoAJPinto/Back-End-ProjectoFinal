#!/usr/bin/python
#Every plataform
from platform import linux_distribution, uname
import sys
import json 

def runscan():
	payload = {}
	if linux_distribution()[1] == ' ':
	  payload["Public Release:"] = linux_distribution()[1]
	for i in range(0, 2):
	  payload[uname()._fields[i]] = uname()[i]
	return payload
