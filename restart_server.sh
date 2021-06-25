#!/bin/sh
cd /societies/caving/CamCavingWeb
killall -u caving gunicorn
pipenv run gunicorn CamCavingWeb.wsgi:application -w4 -b localhost:16589 --timeout 1000 --daemon
