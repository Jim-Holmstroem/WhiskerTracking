all: a0poster.pdf

force:
	pdflatex a0poster.tex

%.pdf: *.tex %.bib
	pdflatex $*
	bibtex $*
	pdflatex $*
	pdflatex $*
