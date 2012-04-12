all: report.pdf

clean:
	rm report.pdf

force: clean all

%.pdf: *.tex
	pdflatex $*.tex
