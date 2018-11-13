#!/bin/bash

set -e

source scripts/env.sh

cd ${sitename}
python manage.py test ilmo_app
cd ..

if [ "$1" == "--teardown" ];
then
    echo "Tearing down testing environment"
    rm -rf ${sitename}
fi
