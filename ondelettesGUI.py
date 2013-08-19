#-------------------------------------------------------------
# Name:        ondelettesGUI.py
# Purpose:     interface graphique du TIPE sur les ondelettes
#
# Author:      Gaetan
#
# Created:     08/08/2013
# Copyright:   (c) Gaetan 2013
# Licence:     CC-BY-SA
#-------------------------------------------------------------

from Tkinter import *
import tkFileDialog, ImageTk
from ondelettes import *
from ttk import Frame, Style
from Tkconstants import *


class Appli(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):

        self.parent.title("Ondelettes GUI")
        self.pack(fill=BOTH, expand=1)
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Ouvrir", command=self.askopenfilename)
        fileMenu.add_command(label="Enregistrer", command=self.asksaveasfilename)
        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="Fichier", menu=fileMenu)

        editMenu = Menu(menubar)
        editMenu.add_command(label="Nuances de gris", command=self.grayscale)
        editMenu.add_command(label="Compresser", command=self.askcompression)
        editMenu.add_command(label="Compresser (new)", command=self.askcompression2)
        editMenu.add_command(label="Resolution 1/2", command=self.onExit)
        menubar.add_cascade(label="Edition", menu=editMenu)

        Style().configure("TFrame", background="#FFF")

    def askopenfilename(self):

        filename = tkFileDialog.askopenfilename(defaultextension = "jpg")
        self.matriceimage = MatriceImage(filename)
        self.image = self.matriceimage.image
        self.imgtk = ImageTk.PhotoImage(self.image)
        self.labelimg = Label(self,image=self.imgtk)
        self.labelimg.image = self.imgtk
        self.labelimg.place(x = 0,y=0)
        self.labelimg.pack()


        self.parent.geometry(str(self.matriceimage.sizex+5)+"x"+str(self.matriceimage.sizey+5)+"+100+300")

    def asksaveasfilename(self):

        filename = tkFileDialog.asksaveasfilename(defaultextension = "jpg")

        self.image.save(filename,'JPEG',quality = 100)

    def askcompression(self):
        global compress
        fen = Tk()
        fen.geometry("300x100+300+300")
        box = DialogScale(fen)
        fen.mainloop()
        fen.destroy()
        self.compression()

    def askcompression2(self):
        global compress
        fen = Tk()
        fen.geometry("300x100+300+300")
        box = DialogScale(fen)
        fen.mainloop()
        fen.destroy()
        self.compression2()

    def compression(self):

        self.matriceimage.getmatrixblue()
        self.matriceimage.getmatrixgreen()
        self.matriceimage.getmatrixred()
        self.matriceimage.create_coef_matrix()
        self.matriceimage.haar()
        self.matriceimage.compression(compress)
        self.matriceimage.syntheselignes()
        self.matriceimage.synthesecolonnes()
        self.labelimg.destroy()

        self.displayimage()

    def compression2(self):


        self.matriceimage.fasthaar(compress, 0, self.matriceimage.sizex, 0, self.matriceimage.sizey)

        self.labelimg.destroy()

        self.displayimage()

    def grayscale(self):
        self.matriceimage.grayscalemeanmatrix()
        self.image = self.matriceimage.makeimagegray(self.matriceimage.matrixgray)
        self.matriceimage.image = self.matriceimage.makeimagegray(self.matriceimage.matrixgray)
        self.labelimg.destroy()

        self.displayimage()

    def displayimage(self):
        self.imgtk = ImageTk.PhotoImage(self.matriceimage.image)
        self.labelimg = Label(self,image=self.imgtk)
        self.labelimg.image = self.imgtk
        self.labelimg.place(x = 0,y=0)
        self.labelimg.pack()
        self.update()

    def onExit(self):
        self.quit()


class DialogScale(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):

        self.parent.title("Compression")
        self.style = Style()
        self.style.theme_use("default")

        self.pack(fill=BOTH, expand=1)

        scale = Scale(self, from_=0, to=255,command=self.onScale, orient= HORIZONTAL)
        scale.place(x=90, y=20)


        self.label2 = Label(self, text="Choisissez un niveau de compression")
        self.label2.place(x=52, y=0)
        self.quitButton = Button(self, text="    Ok    ",command=self.ok)
        self.quitButton.place(x=120, y=65)

    def onScale(self, val):

        self.variable = int(val)

    def ok(self):
        global compress
        compress = self.variable
        self.quit()


def main():

    root = Tk()
    root.geometry("250x250+300+300")
    app = Appli(root)
    root.mainloop()


if __name__ == '__main__':
    main()
