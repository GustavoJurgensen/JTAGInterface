#!/bin/bash
cd interface/src/

echo "Instalando pyqt5"
pip3 install --user pyqt5  
sudo apt-get install python3-pyqt5  
sudo apt-get install pyqt5-dev-tools
sudo apt-get install qttools5-dev-tools

echo "Instalando virtualenv"
pip install virtualenv

echo "Entrando no virtualenv"
python3 -m venv venv
pwd=$PWD
source "$pwd/venv/bin/activate"

echo "Instalando as dependencias no virtualenv"
pip install -r requirements.txt