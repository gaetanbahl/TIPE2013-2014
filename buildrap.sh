echo 'building rapport.pdf'

gnuplot plot.gnu
pdflatex rapport.tex
pdflatex rapport.tex
pdflatex rapport.tex

echo 'done'
