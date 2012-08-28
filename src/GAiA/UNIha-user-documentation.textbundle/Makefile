#
# Makefile for UNIha documentation
#
rev = "$Revision: 1.2 $"

css	=	assets/CSS/GitHub-ReadMe.css
css	=	assets/CSS/i2-Book.css

wkhtmltopdf = /opt/wkhtmltox/bin/wkhtmltopdf
pdfunite	= /usr/bin/pdfunite

UNIha.pdf: coverpage.pdf UNIha-body.pdf
	pdfunite coverpage.pdf UNIha-body.pdf UNIha.pdf

bundle: UNIha.html
	/bin/rm -fr UNIha-documentation
	mkdir UNIha-documentation
	cp -r UNIha.html assets UNIha-documentation
	@tar cvfpz UNIha-doc.tgz UNIha-documentation
	ls -l UNIha-doc.tgz

UNIha.html: UNIha.md Makefile
	@./mk.sh $(css) UNIha.md > UNIha.html

UNIha-body.pdf: UNIha.md UNIha.html
	wkhtmltopdf toc UNIha.html --footer-line --enable-internal-links --footer-spacing 2 --footer-right 'page [page] of [topage]'  UNIha-body.pdf

