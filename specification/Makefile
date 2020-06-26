# Important commands:
#	make update	# download repository version and merge
#	make commit	# upload to repository
#	make check	# spell check
#	make		# generate pdf
#	make bib	# generate bibliogrphy
#	make force	# generate bibliogrphy and force re-run
#	make clean	# remove temp files
#	make spotless   # idem + remove pdf, bib files

# Please do not add .pdf or other generated files to SVN targets.  Thanks!

FILE=csd-rapport

MAKEFLAGS=	--no-print-directory

# ------------------------------
# User configurable dependencies
# ------------------------------

LATEX=pdflatex
BIBTEX=bibtex
SPELLCHECK=aspell
PDFVIEW=open
TEXTEDIT=open

# GNUPlot source files
GPSOURCE= \
	$(wildcard figures/*.gp)

# EPS files included
EPSSOURCE= \
	$(wildcard figures/*.eps)

# PDF files included
PDFSOURCE= \
	$(wildcard figures/*.pdf)

# PNG files included
PNG= \
	$(wildcard figures/*.png)

# BIB files included
BIBS= \
	predef.bib \
	shapiro-bib-ext.bib \
	shapiro-bib-perso.bib
# \
# 	local.bib \
# 	grassroots.bib

# Bibtex style
BST= \
	$(wildcard *.bst)

# .tex file includes or inputs
TEXIN= \
	$(wildcard *.cls) \
	$(wildcard *.sty) \
	$(wildcard tikzfigures/*.tex)

# other file dependencies
DEPS= Makefile

MANUALTARGET=
#	${PNG}
MANUALSOURCE=
#	figures/figures.key

# files that are not Make dependencies but are required nonetheless
OTHERCOMMITS=

# ------------------------------
# End user configurable dependencies
# ------------------------------

EPSGEN=$(GPSOURCE:.gp=.eps)
EPSGRAPHICS= ${EPSGEN} ${EPSSOURCE}

PDFGEN=$(EPSGRAPHICS:.eps=.pdf)
PDFGRAPHICS=${PDFGEN} ${PDFSOURCE}

GRAPHICSSOURCE= ${GPSOURCE} ${EPSSOURCE} ${PDFSOURCE} ${PNG}
GRAPHICSGEN=${EPSGEN} ${PDFGEN}

TEXTDEPS=${FILE}.tex ${TEXIN} ${DEPS}
GRAPHICDEPS= ${PDFGRAPHICS} ${PNG}

SOURCES= ${EPSSOURCE}  ${GPSOURCE}  ${EPSSOURCE}  ${PDFSOURCE}  ${PNG}  ${BIBS}  ${TEXIN} ${BST}
ALLFILES= ${FILE}.tex ${SOURCES} ${DEPS} ${MANUALSOURCE} ${OTHERCOMMITS}

GNUPLOT= gnuplot 

default: etags pdf

# ------------------------------
# source control
# ------------------------------

# Things that are manually derived
${MANUALTARGET}: ${MANUALSOURCE}
	@echo "Must first recreate $@ from $<!!" 2>&1
	@false

pull update:
	# svn update
	git pull

push commit leave:
#	-svn propset svn:keywords 'URL Date Revision Author' ${FILE}.tex
# unset LANG because it influences the way SVN generates the date inside the file
# explicit ${ALLFILES} to verify that they have all been declared by 'svn add'
#	unset LANG; svn commit -m '' ${ALLFILES}
	git add ${ALLFILES}
# also commit files not in dependencies
#	unset LANG; svn commit -m ''
	git commit -a -m '*' --allow-empty
	git pull
	git push origin master

arrive: update edit force show
#	open fig/figures.key

spotless:: clean

check: ${TEXIN}
	# '-d en' tells to use english dictionnary, '-t' is to use LaTeX mode
	# and '-c' is to check.
	$(SPELLCHECK) -d en -t -c $<

# begin diff
# requires latexdiff from http://www.ctan.org/tex-archive/support/latexdiff/
diff: $(FILE)-diff.pdf

remotebase svnbase:
	svn cat $(FILE).tex > $(FILE)-base.tex

localbase base savebase:
	cp $(FILE).tex $(FILE)-base.tex

$(FILE)-diff.tex: $(FILE)-base.tex $(FILE).tex
	latexdiff $(FILE)-base.tex $(FILE).tex > $(FILE)-diff.tex

$(FILE)-diff.aux: $(FILE).aux
	cp $(FILE).aux $(FILE)-diff.aux

$(FILE)-diff.bbl: $(FILE).bbl
	cp $(FILE).bbl $(FILE)-diff.bbl

$(FILE)-diff.pdf: $(FILE)-diff.tex $(FILE)-diff.aux $(FILE)-diff.bbl
	${LATEX} $(FILE)-diff.tex

clean::
	-rm -f $(FILE)-diff.* $(FILE)-base.*

# end diff

# ---------- latex compilation ----------

tags etags: TAGS

TAGS: ${TEXTDEPS}
	etags ${TEXTDEPS}

clean::
	rm -f TAGS

graphics: epsgraphics pdfgraphics

epsgraphics: ${EPSGRAPHICS}

pdfgraphics: ${PDFGRAPHICS}

# dvi: $(FILE).dvi 

edit:
	${TEXTEDIT} ${FILE}.tex

show: pdf
	${PDFVIEW} $(FILE).pdf

pdf: $(FILE).pdf

print lpr: $(FILE).pdf
	lpr $(FILE).pdf

# $(FILE).dvi: $(FILE).tex $(FIGS)

aux: $(FILE).aux

$(FILE).pdf ${FILE}.aux: ${TEXTDEPS} ${GRAPHICDEPS} ${MANUALTARGET}
	${LATEX} $(FILE)

### $(FILE).dvi ${FILE}.aux: ${FILE}.tex ${DEPS} ${EPSGRAPHICS} ${PNG}
### 	latex $(FILE)

#figs:
#		( cd figs; $(MAKE) )
clean::
		/bin/rm -f *~ *.bak *.aux *.log *.toc *.lof *.dvi *.bbl *.blg *.lot *.out
		/bin/rm -rf auto/

spotless:: 
		/bin/rm -f ${FILE}.pdf

# ---------- bibliography ----------

force: bib forcepdf1 forcepdf2

forcepdf1 forcepdf2: FORCE
	${LATEX} $(FILE)

FORCE:

${FILE}.bbl: aux ${BST} ${BIBS} 
	-${BIBTEX} ${FILE}

#		./bibnourl.sh ${BIBS}
#		BIBINPUTS=tmp/:$$BIBINPUTS ${BIBTEX} $(FILE)
#		sed -e 's/%//g' < $(FILE).bbl > $(FILE).bbl~
#		mv $(FILE).bbl~ $(FILE).bbl

# clean::
# 	rm -rf tmp/

bib: $(FILE).bbl 

# effective only for user @shapiro
ifeq ($(shell whoami),shapiro)
commonbibs: shapiro-bib-perso.bib shapiro-bib-ext.bib predef.bib grassroots.bib

shapiro-bib-ext.bib: /Users/shapiro/svnbackup/bib/shapiro-bib-ext.bib
	cp -p /Users/shapiro/svnbackup/bib/shapiro-bib-ext.bib .

shapiro-bib-perso.bib: /Users/shapiro/svnbackup/bib/shapiro-bib-perso.bib
	cp -p /Users/shapiro/svnbackup/bib/shapiro-bib-perso.bib .

predef.bib: /Users/shapiro/svnbackup/bib/predef.bib
	cp -p /Users/shapiro/svnbackup/bib/predef.bib .

short-predef.bib: /Users/shapiro/svnbackup/bib/short-predef.bib
	cp -p /Users/shapiro/svnbackup/bib/short-predef.bib .

grassroots.bib: /Users/shapiro/nobackup/svnstuff/syncfree_SVN/papers/grassroots.bib
	ln -s /Users/shapiro/nobackup/svnstuff/syncfree_SVN/papers/grassroots.bib .

spotless::
	rm -f shapiro-bib-perso.bib shapiro-bib-ext.bib predef.bib short-predef.bib grassroots.bib
endif
# end only @shapiro

# ---------- html ----------

html: ${FILE}.html

${FILE}.html ${FILE}.css: ${FILE}/${FILE}.html
	cp -p ${FILE}/${FILE}.html .
	cp -p ${FILE}/${FILE}.css .

${FILE}/${FILE}.html: ${FILE}.aux
	latex2html -split 0 ${FILE}

clean::
	rm -rf ${FILE}/

spotless::
	rm -f ${FILE}.html ${FILE}.css

# ---------- standard targets ----------

%.eps: %.obj
	tgif -print -eps $^
%.eps: %.gp
	$(GNUPLOT) $^

# %.eps: %.gp dat/%.dat
#	$(GNUPLOT) $^

%.eps: %.fig
	fig2dev -L eps $^ >$@
%.eps: %.prn
	ps2epsi $^ $@
clean::
	rm -f ${GRAPHICSGEN}

%.eps: %.dia
	dia -e $@ $^
%.eps: %.epsraw
	ps2epsi $^ $@

%.pdf: %.tex
	${LATEX} $^

%.bbl: %.aux
	-${BIBTEX} $^

# According to ACM instructions, '-P cmz' embeds Type 1 fonts, which
# enables later PDF generation to be of higher quality 
# %.ps: %.dvi
# 	dvips -P cmz $^ -o
# 	rm -f $@.gz

%.pdf: %.ps
	ps2pdf $^
%.pdf: %.eps
	epstopdf $^

tgz: ${FILE}.pdf
	dir=`basename $$PWD`; \
	tar czvf /tmp/$(FILE).tgz -C .. \
	$(patsubst %,$$dir/%,\
	    ${FILE}.pdf \
	    ${ALLFILES} \
	    ${patsubst %,dat/%,${GPSOURCE:.gp=.dat}}\
	)

# HAL requires .bbl for ArXiV
zip: ${FILE}.pdf ${FILE}.bbl
	rm -rf /tmp/$(FILE).zip; \
	zip /tmp/$(FILE).zip \
	    ${FILE}.pdf \
	    ${ALLFILES} \
	    ${FILE}.bbl \
	    ${patsubst %,dat/%,${GPSOURCE:.gp=.dat}}
