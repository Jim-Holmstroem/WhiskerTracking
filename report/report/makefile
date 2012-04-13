all: report.pdf

clean:
	rm *.aux
	rm *.bbl
	rm *.blg
	rm *.log
	rm *.out
	rm *.toc
	rm report.pdf

force: clean all

run:
	evince report.pdf

%.pdf: *.tex %.bib
	pdflatex $*
	bibtex $*
	pdflatex $*
	pdflatex $*
