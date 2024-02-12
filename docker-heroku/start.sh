#!/bin/bash
sleep 10
source /root/.local/share/virtualenvs/activo-api-*/bin/activate
echo "<<<<<<<<<< Export LANG to the Env>>>>>>>>>>"

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

echo "<<<<<<<< Database Setup and Migrations Starts >>>>>>>>>"
sleep 20
# Run database migrations
flask db upgrade

# Seed database
flask seed

echo " "
echo "<<<<<<<<<<<<<<<<<<<< START API >>>>>>>>>>>>>>>>>>>>>>>>"
gunicorn --workers 1 -t 3600 manage:app --worker-class gevent -b 0.0.0.0:$PORT --access-logfile '-' &

sleep 5
echo " "
# echo "<<<<<<<<<<<<<<<<<<<< START CELERY >>>>>>>>>>>>>>>>>>>>>>>>"
# start Celery worker
# celery worker -A celery_worker.celery_app --loglevel=info &

# start celery beat
# celery -A celery_conf.celery_periodic_scheduler beat --loglevel=info &

echo "<<<<<<<<<<<<<<<<<<<< START DRAMATIQ >>>>>>>>>>>>>>>>>>>>>>>>"
#start dramatiq worker
dramatiq manage