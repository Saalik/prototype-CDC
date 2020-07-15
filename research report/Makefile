INPUTS = tcc-specification.tex
COMPILER = latexmk -pdf

report: 
	$(COMPILER) $(INPUTS)
cleanall:	
	rm -f *.pdf *.out *aux *bbl *blg *log *toc *.ptb *.tod *.fls *.fdb_latexmk *.lof
clean:
	latexmk -c