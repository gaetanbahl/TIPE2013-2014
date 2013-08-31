echo 'building ondelettes.pdf'

gnuplot plot.gnu
pdflatex ondelettes.tex
pdflatex ondelettes.tex
pdflatex ondelettes.tex

echo 'done'
