#!/bin/sh

. /etc/script/lib/command.sh

APKG_PKG_DIR=/usr/local/AppCentral/noip-ddns
PID_FILE=/var/run/noip-ddns.pid
PYTHON_CMD=/usr/local/bin/python3

case $1 in

	start)
		# start DDNS service
		$PYTHON_CMD $APKG_PKG_DIR/data/lib/ddns_updater.py --daemon > /dev/null 2>&1 &
		echo $! > $PID_FILE
		;;

	stop)
		# stop DDNS service
		if [ -f $PID_FILE ]; then
			kill -9 `cat $PID_FILE` 2> /dev/null
			rm -rf $PID_FILE
		fi
		;;

	*)
		echo "usage: $0 {start|stop}"
		exit 1
		;;

esac

exit 0
