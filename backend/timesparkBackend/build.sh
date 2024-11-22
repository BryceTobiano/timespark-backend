#!/bin/bash

# Build the project
echo "Building the project..."
# create a virtual environment named 'venv' if it doesn't already exist
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

echo "Make Migrations..." 
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collect Static..." 
python3 manage.py collectstatic --noinput --clear
