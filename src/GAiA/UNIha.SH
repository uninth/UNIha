:
# Note:
# This is a dummy file. It will be made for real by makeconf. Makeconf will remove
# all existing information every time it runs.
#
# Warning: This file will be sourced by a bash script and must complie with bash syntax

INETIF=""				# Name of internet interface / link interface
COMIF=""				# Name of interface between active and passive firewall
FWCOMIP=""				# Active firewall ip address on COMIF
STANDBYCOMIP=""			# Passive firewall ip address on COMIF
COMNETMASK=""			# Netmask on COMIF

function site_post_f_set_role_to_active() {
	#
	# This will be done after reconfiguration
	#
	/etc/init.d/UNIntpd	restart
	/etc/init.d/dhcpd	restart
	/etc/init.d/dhcrelay	restart
}

function site_post_f_set_role_to_passive() {
	#
	# This will be done after reconfiguration
	#
	/etc/init.d/UNIntpd	restart
	/etc/init.d/dhcpd	restart
	/etc/init.d/dhcrelay	restart
}

# $Header$
