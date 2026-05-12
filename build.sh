#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# load data automatically (IMPORTANT)
python manage.py loaddata data.json || true