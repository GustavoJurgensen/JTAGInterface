#!/bin/bash
cd interface/src/

echo "Entrando no virtualenv, no qual todas as dependencias estão instaladas"
pwd=$PWD
source "$pwd/venv/bin/activate"

echo "Iniciando a UI"
python3 control.py

echo "Fechando a UI"