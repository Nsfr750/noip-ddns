#!/bin/sh

APKG_PKG_DIR=/usr/local/AppCentral/noip-ddns

case "$APKG_PKG_STATUS" in

	install)
		# post install script here
		mkdir -p $APKG_PKG_DIR/etc
		chmod 755 $APKG_PKG_DIR/lib/ddns_updater.py
		;;
	upgrade)
		# post upgrade script here (restore data)
		if [ -d $APKG_TEMP_DIR ]; then
			cp -af $APKG_TEMP_DIR/* $APKG_PKG_DIR/etc/.
		fi
		chmod 755 $APKG_PKG_DIR/lib/ddns_updater.py
		;;
	*)
		;;

esac

exit 0
