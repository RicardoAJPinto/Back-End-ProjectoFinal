#!/usr/bin/python
#Every plataform
from platform import linux_distribution, uname
import sys
import json 

def runscan(payload_zeus):
	payload_zeus["TestResult"] = uname()[1]
	# for i in range(0, 2):
	#   payload_zeus[uname()._fields[i]] = uname()[i]
	payload_zeus["TestResult2"] = uname()[2]
	return payload_zeus
