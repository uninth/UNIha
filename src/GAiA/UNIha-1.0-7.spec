#
# Proto spec for UNIha
#
#

AutoReqProv: no

Requires: UNItools

%define defaultbuildroot /
# Do not try autogenerate prereq/conflicts/obsoletes and check files
%undefine __check_files
%undefine __find_prereq
%undefine __find_conflicts
%undefine __find_obsoletes
# Be sure buildpolicy set to do nothing
%define __spec_install_post %{nil}
# Something that need for rpm-4.1
%define _missing_doc_files_terminate_build 0

%define name    UNIha
%define version 1.0
%define release 7

Summary: Utility for check firewall firewall and nat rule
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL
Group: root
Packager: Niels Thomas Haugaard, nth@i2.dk

%description
Check and visualize changes to firewall and NAT rules in for GaIA, R76 and R77*

# Everything is installed 'by hand' below UNIha_rootdir
%prep
ln -s /lan/ssi/shared/software/internal/UNIha/src/GAiA/UNIha_rootdir /tmp/UNIha_rootdir

%clean
rm /tmp/UNIha_rootdir

# post install script -- just before %files
%post

cat <<-EOF > /tmp/UNIha.adduser.clish
add user reconfig uid 0 homedir /home/UNIha
add rba user reconfig roles adminRole
set user reconfig shell /bin/bash
EOF

cp		/home/admin/.bash*	/home/UNIha/
cp -r	/home/admin/.ssh	/home/UNIha/

# ignore errors save config
clish -i -s -f /tmp/UNIha.adduser.clish

/bin/rm -f /tmp/UNIha.adduser.clish
cat << 'EOF' > /home/UNIha/.bashrc
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific aliases and functions
. $HOME/bin/reconfig_menu
EOF

# pre uninstall script
%preun

clish -sc "delete user reconfig"

echo "Removing cron files ... "
/bin/rm -f /etc/cron.d/UNIha_prob /etc/cron.d/UNIha_settime /etc/cron.d/UNIha_update
/etc/init.d/crond restart

# All files below here - special care regarding upgrade for the config files
%files
/home/UNIha
%config /home/UNIha/etc/UNIha.SH
