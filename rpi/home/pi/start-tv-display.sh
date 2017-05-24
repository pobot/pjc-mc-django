#!/bin/bash

SERVER=eric-laptop.local
START_BROWSER="chromium-browser --kiosk --incognito --disable-infobars http://$SERVER:8000/display"

while true ; do
    echo "Waiting for $SERVER..."
    ping -c 1 $SERVER >/dev/null 2>&1
    if [ $? -eq 0 ] ; then
        echo -e "... server online\nLaunching kiosk..."
        $START_BROWSER
        exit 0
    fi
    sleep 1
done

