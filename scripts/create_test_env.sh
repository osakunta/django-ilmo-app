#!/bin/bash

set -e
source scripts/env.sh

echo "Creating test environment"

echo "Installing requirements..."
pip install -r requirements.txt

echo "Creating test site"
sitename=testsite
djangocms ${sitename}
cd ${sitename}
ln -s ../ilmo_app ilmo_app

settings_file=${sitename}/settings.py
sed -i .bak 's/INSTALLED_APPS =.*/&"ilmo_app",/' ${settings_file}
rm ${settings_file}.bak

echo "Done"
