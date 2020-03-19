#!/bin/sh 

if [ "$DATABASE" = "mysql" ]; then
    echo "Wait MySQL start"

    while ! $(curl $SQL_HOST:$SQL_PORT -o /dev/null -s); do
        sleep 0.1
        echo "Waitting..."
    done

    echo "MySQL started"
fi

python blog/manage.py flush --no-input
python blog/manage.py migrate
python blog/manage.py collectstatic --no-input --clear

exec "$@"
