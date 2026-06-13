#!/usr/bin/env bash

pip install -r requirements.txt

python ./gcs/manage.py collectstatic --noinput

python ./gcs/manage.py migrate