#
# Regular cron jobs for the vaporos-flatpak-manager package
#
0 4	* * *	root	[ -x /usr/bin/vaporos-flatpak-manager_maintenance ] && /usr/bin/vaporos-flatpak-manager_maintenance
