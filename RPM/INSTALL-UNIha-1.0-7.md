
#Installation procedure for UNIha-1.0-7.i386.rpm
    Package name: UNIha-1.0-7.i386.rpm
    Version     : 1.0
    Release     : 7

## Prerequisite

1. Two identical server grade machines - BIOS, RAID, etc. - with the
   relevant software from Check Point installed but only configured with
   a minimal configuration (external interface, default gateway, admin user
   and the relevant Check Point software installed but not configured).

1. A dedicated interface - not VLAN - on each machine, connected with a patch cable.

1. The package ``UNItools`` must also be installed, as ``perl`` is required for ``UNIha``. This will also
   enable ``sshd`` and modify ``/etc/scpusers`` as needed.

## Installation

1. Define a interface (not VLAN) with at least two IP addresses.
   Label one _active_ and an other _passive_. The LAN will be
   used for backup/restore syncronisation and should not be used
   for anything else.

|Host     |Internet Interface  |Sync Interface | IP addr on sync interface | Netmask on sync interface |
| ------- | ------------------ | ------------- | ------------------------- | ------------------------- |
|active   |                    |               |                           |                           |
|passive  |                    |               |                           |                           |

1. **Finish the installation** of the firewall and the IP configuration on the first host (**active firewall**). 
   The machine should have the IP address of the _active firewall_.    
   **Important**: The _passive firewall_ must have access with ``ssh`` to the _active firewall_.

1. Copy ``UNIha-1.0-7.i386.rpm`` to the _active firewall_, and install the rpm, but do not run ``makeconf``

        td -x UNIha-1.0-7.i386.rpm external-interface
        td external-interface
        rpm -Uvh /var/tmp/UNIha-1.0-7.i386.rpm

1. Make a backup of the _active firewall_ and monitor the progress:

         clish -c "add backup local"
         watch "clish -c 'show backup status'"

   Stop ``watch``when the backup is done. The backup archive ends in either ``/var/CPbackup/backups``
   (open server) or ``/vas/log/CPbackups/backups`` (appliances).

1. **Continue with the _passive firewall_**. Find the interface which is connected to the _active firewall_,
   the _sync interface_.  
   It may not (yet) be in the same location as on the _active firewall_. Use the commands below or stay with ``ethtool``:

`````
cat << 'EOF' > /tmp/linkstatus.sh
printf "%10s\t%-10s\t\t\t%-25s\n" "Interface" "Link status" "IPv4 addr"
IFNAMES=`ifconfig -a|sed '/^[ 	]/d; s/[  ].*//; /^$/d; /^lo$/d; /sit/d'`
for IFNAME in $IFNAMES
do
	ifconfig ${IFNAME} up
	IPv4=`ifconfig ${IFNAME} |sed '/inet addr/!d; s/.*addr://; s/[ 	].*Mask:/\//'`
	STATUS=`ethtool ${IFNAME} | sed '/Link/!d; s/^[ \t]*//;s/[ \t]*$//'`
	printf "%10s\t%-10s\t/\t%25s\n" ${IFNAME} "${STATUS}"  "${IPv4}"
done
EOF
chmod 755 /tmp/linkstatus.sh && watch /tmp/linkstatus.sh
`````

1. Once the interface is found  on the _passive firewall_ stop the firewall software and re-configure the sync interface 

        cpstop 
        /sbin/ifconfig interface cidr/len 

Copy the _backup archive_ and the _rpm_ files for _UNIha_ and _UNItools_ from the 
   _active firewall_ to the _passive firewall_:

     scp admin@active:/path/to/files ... /var/tmp

and install ``UNItools`` and ``UNIha``. Restore the backup, by moving the _backup archive_ to the same default location on the _passive fireall_ as on the _active firewall_, and execute the command:

        set backup restore local <TAB>

which will expand to the archive made on the _active firewall_. If that fails see sk91400. The _passive firewall_ may re-boot when the restore fnishes.

### Milestone: Now you have two identical machines

## Setting up the _passive firewall_

1. On the (former) _passive firewall_ execute the commands

        cpstop 
        /sbin/ifconfig interface cidr/len 

1. On the _active firewall_ execute the command

       /home/UNIha/bin/makeconf

   and follow the on-screen instructions. ``makeconf`` asks for 
   * Internet infterface
   * sync interface

   and writes answers to the configuration file ``/home/UNIha/etc/UNIha.SH``. The file will
   be deleted and re-written everytime ``makeconf`` is executed.

   ``makeconf`` will 
   * enable _ssh keys_ (login without password) between the two hosts
   * install tree ``cron`` entries in ``/etc/cron.d/``:
     * to test if the remote wants to change role (once a minute),
	 * check if the firewall configuration has changed and must be backed up and restored (each quarter) and
	 * two times a day sync time as the passive firewall may not have Internet access.


1. Once the _active firewall_ and the _passive firewall_ are configured the status can be tested with

        /home/UNIha/bin/UNIha check

## Known errors and limitations

   * The GUI (CPMI) prevents backup when open; please close the CPMI session when it is no longer needed.
   * When the fireall re-boots it takes between 10 and 15 min. before the _passive firewall_ decides it is not
     a firewall and re-configure itself as the _passive firewall_ (no software running, ip-reconfiguration).
   * ``ssh keys`` will fail at some point despite the efford made by ``UNIha``. ``ssh`` connections between the
   _active firewall_ and the _passive firewall_ is made to the ``ip addresses`` while humans may prefer the
   names given in ``/etc/hosts``.

Finally Check Point patching has to be in sync; and patches has to applied the
same way on both the passive and active host.

## Uninstallation

Remove the package with:

	rpm -e --nodeps UNIha-1.0-7.i386.rpm

## Note

This document is in RCS and build with make

# RPM info

View rpm content with

    rpm -lpq UNIha-1.0-7.i386.rpm
