all: a0poster.pdf

clean:
	rm a0poster.pdf

force: clean a0poster.pdf

%.pdf: *.tex %.bib
	cp --remove-destination ../report/report.bib a0poster.bib
	pdflatex $*
	bibtex $*
	pdflatex $*
	pdflatex $*
