#------------------------------------------------------------
# Name:        ondelettes.py
# Purpose:     definition de classes de traitement d'image
#
# Author:      gaetan
#
# Created:     10/07/2013
# Copyright:   (c) Gaetan 2013
# Licence:     CC-BY-SA
#------------------------------------------------------------

import Image, math

class Matrice:

    def __init__(self,x,y,what):
        self.tableau = []
        self.x, self.y = x,y

        for i in range(self.x):
            self.tableau.append([])
            for j in range(self.y):
                self.tableau[i].append(what)

    def transpose(self):
        self.tableau = [[row[i] for row in self.tableau] for i in range(self.y)]
        self.x,self.y = self.y,self.x

    def add(self,matrice):

        for i in range(n):
            for j in range(p):
                self.tableau[i][j] += matrice.tableau[i][j]

    def multiply(self,matrice):

        for i in range(self.x):
            for j in range(self.y):
                somme = 0
                for k in range(self.y):
                    somme += self.tableau[i][k]*matrice.tableau[k][j]

    def copy(self,matrice):

        for i in range(self.x):
            for j in range(self.y):
                self.tableau[i][j] = matrice.tableau[i][j]

    def update(self):
        self.x = len(self.tableau)
        self.y = len(self.tableau[0])



class MatriceImage():

    def __init__(self,lienimage):
        self.lienimage = lienimage
        self.image = Image.open(lienimage)
        self.pix = self.image.load()
        self.sizex,self.sizey = self.image.size
        self.matrice = Matrice(self.sizex,self.sizey,self.pix[0,0])
        self.fill()

    def fill(self):
        for i in range(self.sizex):
            for j in range(self.sizey):
                self.matrice.tableau[i][j] = self.pix[i,j]

    def grayscalemean(self):
        for i in range(self.sizex):
            for j in range(self.sizey):
                mean = (self.pix[i,j][0] + self.pix[i,j][1] + self.pix[i,j][2])/3
                self.pix[i,j] = (mean,mean,mean)

    def grayscalemeanmatrix(self):
        self.matrixgray = Matrice(self.sizex,self.sizey,0)
        for i in range(self.sizex):
            for j in range(self.sizey):
                mean = (self.pix[i,j][0] + self.pix[i,j][1] + self.pix[i,j][2])/3
                self.matrixgray.tableau[i][j] = mean

    def getmatrixred(self):
        self.matrixred = Matrice(self.sizex,self.sizey,self.pix[0,0][0])
        for i in range(self.sizex):
            for j in range(self.sizey):
                self.matrixred.tableau[i][j] = self.matrice.tableau[i][j][0]

    def getmatrixblue(self):
        self.matrixblue = Matrice(self.sizex,self.sizey,self.pix[0,0][2])
        for i in range(self.sizex):
            for j in range(self.sizey):
                self.matrixblue.tableau[i][j] = self.matrice.tableau[i][j][2]

    def getmatrixgreen(self):
        self.matrixgreen = Matrice(self.sizex,self.sizey,self.pix[0,0][1])
        for i in range(self.sizex):
            for j in range(self.sizey):
                self.matrixgreen.tableau[i][j] = self.matrice.tableau[i][j][1]

    def save(self,nom):
        self.image.save(nom)

    def ondelette_haar(self,tableau_valeurs,ordre):
        longueur = len(tableau_valeurs)
        coeff_approx, coeff_ondelettes = [],[]
        for i in range(longueur/2):

            coeff_approx.append((tableau_valeurs[2*i] + tableau_valeurs[2*i+1])/2)
            coeff_ondelettes.append((tableau_valeurs[2*i] - tableau_valeurs[2*i+1])/2)

        if ordre == 1:
            return coeff_approx,coeff_ondelettes
        else:
            return ondelette_haar(coeff_approx,ordre -1),coeff_ondelettes

    def getcolonne(self,tab,num):
        col = []
        for i in range(len(tab)):
            col.append(tab[i][num])
        return col

    def setcolonne(self,matrice,tab,num):
        for i in range(len(tab)):
            matrice[num][i] = tab[i]

    def getligne(self,tab,num):
        return tab[num]

    def apply_haar_lig(self,matrice,chiffre):
        for i in range(len(matrice)):
            matrice[i] = self.ondelette_haar(matrice[i],1)[chiffre]

    def apply_haar_col(self,matrice):
        for i in range(len(matrice[0])):
            col = self.getcolonne(matrice,i)
            col = self.ondelette_haar(col,1)[0]
            self.setcolonne(matrice,col,i)

    def makeimagegray(self,matriceimage):
        matriceimage.update()
        im = Image.new("RGB", (matriceimage.x, matriceimage.y), "white")
        pix = im.load()

        for i in range(matriceimage.x):
            for j in range(matriceimage.y):
                pix[i,j] = (int(matriceimage.tableau[i][j]),int(matriceimage.tableau[i][j]),int(matriceimage.tableau[i][j]))
        return im

    def haar_grayscale(self):
        self.grayscalemeanmatrix()

        self.apply_haar_lig(self.matrixgray.tableau,0)
        self.matrixgray.update()
        self.matrixgray.transpose()
        self.matrixgray.update()
        self.apply_haar_lig(self.matrixgray.tableau,0)
        self.matrixgray.update()
        self.matrixgray.transpose()
        self.imagehaargray = self.makeimagegray(self.matrixgray)

    def update(self):
        self.sizex = matrice.x
        self.sizey = matrice.y

    def create_coef_matrix(self):
        self.matrixcoefr = Matrice(self.matrixred.x,self.matrixred.y,0)
        self.matrixcoefg = Matrice(self.matrixred.x,self.matrixred.y,0)
        self.matrixcoefb = Matrice(self.matrixred.x,self.matrixred.y,0)
        self.matrixcoefr.copy(self.matrixred)
        self.matrixcoefg.copy(self.matrixgreen)
        self.matrixcoefb.copy(self.matrixblue)

    def haar(self):

        for i in [self.matrixred,self.matrixgreen,self.matrixblue]:
            self.apply_haar_lig(i.tableau,0)
            i.update()
            i.transpose()
            i.update()
            self.apply_haar_lig(i.tableau,0)
            i.update()
            i.transpose()

        for i in [self.matrixcoefr,self.matrixcoefg,self.matrixcoefb]:
            self.apply_haar_lig(i.tableau,1)
            i.update()
            i.transpose()
            i.update()
            self.apply_haar_lig(i.tableau,1)
            i.update()
            i.transpose()

    def makeimage(self):
        im = Image.new("RGB", (self.matrixred.x, self.matrixred.y), "white")
        pix = im.load()

        for i in range(self.matrixred.x):
            for j in range(self.matrixred.y):
                pix[i,j] = (int(self.matrixred.tableau[i][j]),int(self.matrixgreen.tableau[i][j]),int(self.matrixblue.tableau[i][j]))
        return im

    def compression(self,epsilon):
        for tab in [self.matrixcoefr.tableau,self.matrixcoefg.tableau,self.matrixcoefb.tableau]:
            for i in tab:
                for j in i:
                    if abs(i) < epsilon:
                        i = 0
def main():
    image = MatriceImage("chat.jpg")
    image.getmatrixblue()
    image.getmatrixgreen()
    image.getmatrixred()
    image.create_coef_matrix()
    #image.grayscalemeanmatrix()
    #image.makeimagegray(image.matrixgray).save("piano_gris.jpg")
    image.haar()
    image.makeimage().save("chat_reduit_couleur.jpg")
    print image.matrixcoefr.tableau

if __name__ == '__main__':
    main()
