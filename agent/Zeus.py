#!/usr/bin/python
import schedule
import time

import DetectOS

def scan():
    DetectOS.OperatingSystem()
    print("Done +1 post")

schedule.every(1).minute.do(scan)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)

while True:
    schedule.run_pending()
    