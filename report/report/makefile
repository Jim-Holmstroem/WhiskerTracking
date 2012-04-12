all: report.pdf

clean:
	rm report.pdf

force: clean all

run:
	evince report.pdf

%.pdf: *.tex
	pdflatex $*.tex
