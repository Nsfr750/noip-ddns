#!/bin/sh

. /etc/script/lib/command.sh

APKG_PKG_DIR=/usr/local/AppCentral/noip-ddns
PID_FILE_DDNS=/var/run/noip-ddns.pid
PID_FILE_WEB=/var/run/noip-ddns-web.pid
PYTHON_CMD=/usr/local/bin/python3

case $1 in

	start)
		# start DDNS service
		$PYTHON_CMD $APKG_PKG_DIR/data/lib/ddns_updater.py --daemon > /dev/null 2>&1 &
		echo $! > $PID_FILE_DDNS
		
		# start web server
		$PYTHON_CMD $APKG_PKG_DIR/data/lib/web_server.py > /dev/null 2>&1 &
		echo $! > $PID_FILE_WEB
		;;

	stop)
		# stop DDNS service
		if [ -f $PID_FILE_DDNS ]; then
			kill -9 `cat $PID_FILE_DDNS` 2> /dev/null
			rm -rf $PID_FILE_DDNS
		fi
		
		# stop web server
		if [ -f $PID_FILE_WEB ]; then
			kill -9 `cat $PID_FILE_WEB` 2> /dev/null
			rm -rf $PID_FILE_WEB
		fi
		;;

	*)
		echo "usage: $0 {start|stop}"
		exit 1
		;;

esac

exit 0
