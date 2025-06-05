#!/bin/sh

if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for mysql..."

    while ! nc -z $MYSQL_HOST $MYSQL_PORT; do
      sleep 0.1
    done

    echo "MySQL started"
fi

python manage.py flush --no-input
python manage.py migrate

exec "$@"