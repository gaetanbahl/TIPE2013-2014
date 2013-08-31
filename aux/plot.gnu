set terminal latex
set output 'graph.tex'
set autoscale
set xtics auto
set ylabel "\\rotatebox{90}{Temps de compression (s)}"
set xlabel "Taille de l'image (px/2)"
#set ylabel 'Temps de compression (s)'

plot 'bench.txt' using 1:2 notitle with lines
