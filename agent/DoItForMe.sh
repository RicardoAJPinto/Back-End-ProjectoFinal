#!/bin/bash
# Script to install all packages needed for Zeus
Color_Off='\033[0m'       # Text Reset

# Regular Colors
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan

echo -e "$Cyan \n Updating and Upgrading system.. $Color_Off"
sudo apt-get update
sudo apt-get upgrade

#sudo apt-get install -y python3-pip
echo -e "$Cyan \n Updating and Upgrading system.. $Color_Off"
python get-pip.py
#sudo apt install python-pip

echo -e "$Cyan \n Installing needed packages.. $Color_Off"
pip install -r requirements.txt