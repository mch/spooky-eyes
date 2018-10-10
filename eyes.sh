#!/bin/bash

start() {
    /home/pi/Work/spooky-eyes/SpookyEyes/spooky-eyes.py &
    PID=$!
    echo $PID > /var/run/spookyeyes.pid
}

stop() {
    PID=`cat /var/run/spookyeyes.pid`
    kill -2 $PID
}

case $1 in
    start|stop) "$1" ;;
esac

