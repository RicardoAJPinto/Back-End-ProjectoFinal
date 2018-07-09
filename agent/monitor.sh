#!/bin/bash
# Description:
# Starts python script and restarts it if it crashes 
# but doesn't restart if the script exits normally

until Zeus.py; do
    echo "'Zeus.py' crashed with exit code $?. Restarting..." >&2
    sleep 1
done
