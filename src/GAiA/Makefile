##########################################################################################
#
# Makefile for UNIha
#
##########################################################################################

VERSION		= 1.0
RELEASE		= 7

HOSTNAME	= `hostname`

TARGETDIR	= /lan/ssi/shared/software/internal/UNIha
WORKDIR		= $(TARGETDIR)/src/GAiA

ROOTDIR		= $(WORKDIR)/UNIha_rootdir
GROUP		= root
NAME		= UNIha

ARCH		= i386
REDHAT		= /usr/src/redhat
BUILDDIR	= $(REDHAT)/RPMS/$(ARCH)/
SPFILE		= UNIha-$(VERSION)-$(RELEASE).spec
SPTEMPLATE	= uniha.spec.template
SPECFILE	= $(REDHAT)/SPECS/$(SPFILE)
RPMBR		= /tmp/UNIha_rootdir

TARGET		= $(NAME)-$(VERSION)-$(RELEASE).$(ARCH).rpm
INSTALL		= INSTALL-$(NAME)-$(VERSION)-$(RELEASE).md
INST_HTML	= INSTALL-$(NAME)-$(VERSION)-$(RELEASE).html

RPMDIR		= ../../RPM

DOCS		= about.txt README LICENSE unix_design.txt README.R77.30 contact_information.txt
UNIHACFG	= UNIha.SH
EXTBIN		= ethwireck-1.3/ethwireck
CPBIN		= disconnect_client
BIN			= UNIha UNIhadaemon UNIhad makeconf reconfig_menu

HOMEDIR		= /home/UNIha
BINDIR		= $(HOMEDIR)/bin
DOCDIR		= $(HOMEDIR)/docs
LOGDIR		= $(HOMEDIR)/log
TMPDIR		= $(HOMEDIR)/tmp
ETCDIR		= $(HOMEDIR)/etc
USER		= reconfig
UID			= 8888


all: $(TARGET)

#
# Installation instruction
#
$(INSTALL): INSTALL.md
	@sed "									\
		s/__VERSION__/$(VERSION)/g;			\
		s/__RELEASE__/$(RELEASE)/g;			\
		s%__TARGET__%$(TARGET)%g;			\
		" < INSTALL.md > $(INSTALL)

# updatewiki: $(INSTALL)
#		# copy user documentation to wiki
#		ssh root@office 'cd /var/www/volatile/software/uniha && /bin/rm -fr *pdf UNIha-documentation'
#		mkd2html -css UNIha-documentation/assets/CSS/i2-Book.css $(INSTALL)	# makes $(INST_HTML)
#		scp $(INST_HTML) root@office:/var/www/volatile/software/uniha/INSTALL.html
#		cd ./UNIha-user-documentation.textbundle && rsync -avzH -e ssh UNIha.html UNIha.pdf assets root@office:/var/www/volatile/software/uniha/UNIha-documentation/
#		cd ./UNIha-user-documentation.textbundle && rsync -avzH -e ssh assets/img/coverpage.png root@office:/var/www/dokuwiki/data/media/firewall_support/gaia_pkgs/
#

#
# Check make runs on the right compile host
#
check:
	@if [ -d $(TARGETDIR) ]; then echo targetdir ok; else echo targetdir not found; exit 1; fi
	@if [ -d $(WORKDIR) ]; then echo wokdir ok; else echo workdir $(WORKDIR) not found; exit 1; fi
	@echo $@ done

#
# Build the version specific RPM spec file
#
$(SPFILE): check $(SPTEMPLATE)
	@sed "									\
		s/__VERSION__/$(VERSION)/g;			\
		s/__RELEASE__/$(RELEASE)/g;			\
		s%__ROOTDIR__%$(ROOTDIR)%g;			\
		s%__RPMBR__%$(RPMBR)%g;				\
		" < $(SPTEMPLATE)  > $(SPFILE)
	@echo $@ done

#
# Build the RPM package
#
build: $(INSTALL) $(SPFILE) Makefile
	@rsync --delete-after -avzH /home/UNIha UNIha_rootdir/home
	@rpmbuild -bb --buildroot=$(RPMBR) $(SPFILE)
	@mv $(BUILDDIR)/$(NAME)-$(VERSION)-$(RELEASE).$(ARCH).rpm .

#
# Info during build
#
info: build
	@echo "rpm content: rpm -lpq $(NAME)-$(VERSION)-$(RELEASE).$(ARCH).rpm"
	@echo "rpm install: rpm -Uvh $(NAME)-$(VERSION)-$(RELEASE).$(ARCH).rpm"

#
# Move installation instruction and rpm to a known place
#
$(TARGET): $(BIN) $(DOC) Makefile
	$(MAKE) dirs bin etc docs info build
	@/bin/rm -f $(TARGETDIR)/$(TARGET) $(TARGETDIR)/$(INSTALL)
	@/bin/rm -f $(RPMDIR)/$(TARGET) $(RPMDIR)/$(INSTALL)
	mv $(INSTALL) $(RPMDIR)/
	mv $(TARGET) $(RPMDIR)/

clean:
	/bin/rm -fr  *.bak /home/UNIha $(RPMBR)

#
# Build everything below /home/UNIha on localhost
#
install_in_home:
	$(MAKE) dirs bin etc docs 

dirs:
	mkdir -p		$(HOMEDIR) $(BINDIR) $(DOCDIR) $(LOGDIR) $(TMPDIR) $(ETCDIR)
	chmod -R 700	$(HOMEDIR)
	chown -R		$(UID) $(HOMEDIR) 

bin: $(BIN) $(CPBIN)
	install $(BIN) -m 555 -o $(UID) $(BINDIR)

etc: $(UNIHACFG)
	install $(UNIHACFG) -m 644 -o $(UID) $(ETCDIR)

docs: $(DOCS)
	install $(DOCS) -m 444 -o $(UID) $(DOCDIR)

ethwireck: ethwireck-1.3/ethwireck.c
	wget -N http://pepper.linuxfocus.org/~guido/ethwireck-1.3.tar.gz
	tar xvfpz ethwireck-1.3.tar.gz
	cd ethwireck-1.3 && $(MAKE) clean all
	mv ethwireck-1.3/ethwireck .
	# install ethwireck-1.3/ethwireck $(BINDIR)
	
# http://pepper.linuxfocus.org/~guido/#ethwireck
# http://pepper.linuxfocus.org/~guido/ethwireck-1.3.tar.gz

