#!/usr/bin/python

import datetime
 
with open('dateInfo.txt','a') as outFile:
    outFile.write('\nAcessed on:' + str(datetime.datetime.now()))