#!/bin/bash

# this script is used to boot a Docker container
cd /var/www/html
echo "I am Here.........starting while"
pip3 install --upgrade pip
pip3 install -r requirements.txt
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done


echo "I am Here.........DONE while"

exec gunicorn -b :5000 --access-logfile - --error-logfile - run:app
