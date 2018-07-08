#!/bin/bash
# Description:
# Starts python script and restarts it if it crashes 
# but doesn't restart if the script exits normally

until zeus.py; do
    echo "'myscript.py' crashed with exit code $?. Restarting..." >&2
    sleep 1
done

#Then just start the monitor script in background:
# nohup monitor.sh &

# continue script after reboot: 
# Linux:
# crontab -e
# @reboot  /path/to/job