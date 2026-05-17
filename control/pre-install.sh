#!/bin/sh

APKG_PKG_DIR=/usr/local/AppCentral/noip-ddns

case "$APKG_PKG_STATUS" in

	install)
		# pre install script here
		;;
	upgrade)
		# pre upgrade script here (backup data)
		if [ -d $APKG_PKG_DIR/etc ]; then
			cp -af $APKG_PKG_DIR/etc/* $APKG_TEMP_DIR/.
		fi
		;;
	*)
		;;

esac

exit 0
