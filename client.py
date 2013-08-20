#-------------------------------------------------------------
# Name:        client.py
# Purpose:     client du TIPE sur les ondelettes
#
# Author:      Gaetan
#
# Created:     20/08/2013
# Copyright:   (c) Gaetan 2013
# Licence:     CC-BY-SA
#-------------------------------------------------------------

import socket
import Image

def sendImage(socket,link):
        image = Image.open(link)
        pix = image.load()
        x,y = image.size
        string = "sendimg " + str(x) + " " + str(y) + " " + link
        socket.send(string.encode('ascii'))
        reply = socket.recv(32)
        if reply == b"ok":
                for i in range(x):
                        for j in range(y):
                                r,g,b = pix[i,j]
                                pixel = str(i) + " " + str(j) + " " + str(r) + " " + str(g) + " " + str(b)
                                print pixel
                                leng = str(len(pixel))
                                print leng
                                socket.send(leng.encode('ascii'))
                                socket.send(pixel.encode('ascii'))
        
        socket.send(b"end")            
        reply = socket.recv(32)
        
        return reply


def storeImage(link):
        image = Image.open(link)
        pix = image.load()
        x,y = image.size
        
        im = Image.new("RGB", (x / 2, y / 2), "white")
        pi = im.load()
        
        for i in range(x / 2):
                for j in range(y / 2):
                        r = (((pix[2 * i, 2 * j][0] + pix[2 * i + 1, 2 * j][0]) / 2) + ((pix[2 * i, 2 * j + 1][0] + pix[2 * i + 1, 2 * j + 1][0]) / 2)) / 2
                        g = (((pix[2 * i, 2 * j][1] + pix[2 * i + 1, 2 * j][1]) / 2) + ((pix[2 * i, 2 * j + 1][1] + pix[2 * i + 1, 2 * j + 1][1]) / 2)) / 2
                        b = (((pix[2 * i, 2 * j][2] + pix[2 * i + 1, 2 * j][2]) / 2) + ((pix[2 * i, 2 * j + 1][2] + pix[2 * i + 1, 2 * j + 1][2]) / 2)) / 2
                        pi[i, j] = (r,g,b)
                        
        image.save("stor" + link, 'JPEG', quality = 100)
        
        
def main():

        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion.connect(('localhost', 13337))
        sendImage(connexion, 'chatongris.jpg')
        connexion.close()
        

if __name__ == "__main__":
        main()
