#---------------------------------------------------------
# Name:        bench.py
# Purpose:     benchmarking d'algorithmes
#
# Author:      gaetan
#
# Created:     19/08/2013
# Copyright:   (c) Gaetan 2013
# Licence:     CC-BY-SA
#---------------------------------------------------------


import Image
import time
import random
from ondelettes import *


def image_gen(x):
    im = Image.new("RGB", (x, x), "white")
    return im


def randomize(pix, x):
    for i in range(x):
        for j in range(x):
            pix[i, j] = (random.randrange(255), random.randrange(255),
             random.randrange(255))


def bench_square(ran):

    for i in ran:
        image = image_gen(2 * i)
        pix = image.load()
        randomize(pix, 2 * i)
        start = time.time()
        fasthaar(pix, 0, 0, 2 * i, 0, 2 * i)
        end = time.time()
        print str(i) + " " + str(end - start)


def fasthaar(pix, epsilon, xa, xb, ya, yb):

    for x in range(xa / 2, xb / 2):

        for y in range(ya / 2, yb / 2):

            carres = []

            for i in range(3):
                carres.append([[pix[2 * x, 2 * y][i], pix[2 * x, 2 * y + 1][i]],
                     [pix[2 * x + 1, 2 * y][i], pix[2 * x + 1, 2 * y + 1][i]]])

            ondlhaut = [(carres[i][0][0] - carres[i][1][0]) / 2
             for i in range(3)]
            ondlbas = [(carres[i][0][1] - carres[i][1][1]) / 2
             for i in range(3)]

            for i in range(3):
                carres[i][0][0] = (carres[i][0][0] + carres[i][1][0]) / 2
                carres[i][0][1] = (carres[i][0][1] + carres[i][1][1]) / 2

            ondlmix = [(carres[i][0][0] - carres[i][0][1]) / 2
              for i in range(3)]

            for i in range(3):
                carres[i][0][0] = (carres[i][0][0] + carres[i][0][1]) / 2

            for i in range(3):
                if abs(ondlmix[i]) < epsilon:
                    carres[i][0][1] = carres[i][0][0]
                else:
                    carres[i][0][1] = carres[i][0][0] - ondlmix[i]
                    carres[i][0][0] = carres[i][0][0] + ondlmix[i]

                if abs(ondlhaut[i]) < epsilon:
                    carres[i][1][0] = carres[i][0][0]
                else:
                    carres[i][1][0] = carres[i][0][0] - ondlhaut[i]
                    carres[i][0][0] = carres[i][0][0] + ondlhaut[i]

                if abs(ondlbas[i]) < epsilon:
                    carres[i][1][1] = carres[i][0][1]
                else:
                    carres[i][1][1] = carres[i][0][1] - ondlbas[i]
                    carres[i][0][1] = carres[i][0][1] + ondlbas[i]

            for i in [2 * x, 2 * x + 1]:
                for j in [2 * y, 2 * y + 1]:
                    pix[i, j] = (carres[0][i - 2 * x][j - 2 * y],
                     carres[1][i - 2 * x][j - 2 * y],
                     carres[2][i - 2 * x][j - 2 * y])


def main():
    bench_square(range(1,1000))


if __name__ == '__main__':
    main()
