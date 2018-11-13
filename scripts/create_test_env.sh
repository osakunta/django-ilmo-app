#!/bin/bash

set -e
source scripts/env.sh

echo "Creating test environment"

if [ "$1" == "--install-requirements" ];
then
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

echo "Creating test site"
sitename=testsite
djangocms ${sitename}
cd ${sitename}
ln -s ../ilmo_app ilmo_app

settings_file=${sitename}/settings.py

pattern="s/INSTALLED_APPS =.*/&'ilmo_app',/"

case "$(uname -s)" in
  Darwin)
      sed -i .bak "${pattern}" ${settings_file}
      rm ${settings_file}.bak
      ;;
  Linux)
      sed -i "${pattern}" ${settings_file}
      ;;
  *)
     exit 1
     ;;
esac

echo "Done"
