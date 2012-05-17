all: report.pdf

clean:
	rm -f *.aux
	rm -f *.bbl
	rm -f *.blg
	rm -f *.log
	rm -f *.out
	rm -f *.toc
	rm -f report.pdf

force: clean all

run:
	evince report.pdf

%.pdf: *.tex *.bib
	pdflatex report.tex
	bibtex report
	pdflatex report.tex
	pdflatex report.tex
