#!/usr/bin/python2
#-------------------------------------------------------------
# Name:        client.py
# Purpose:     client du TIPE sur les ondelettes
#
# Author:      Gaetan Bahl
#
# Created:     20/08/2013
# Copyright:   (c) Gaetan Bahl 2013
# Licence:     CC-BY-SA
#-------------------------------------------------------------

import socket
import Image
import time
import struct
import sys

def sendImage(socket,link):
    image = Image.open(link)
    pix = image.load()
    x,y = image.size
    string = "sendimg " + str(x) + " " + str(y) + " " + link
    socket.send(string.encode('ascii'))
    reply = socket.recv(32)
    if reply == b"ok":
        t = ""
        for i in range(x):

            for j in range(y):
                r,g,b = pix[i,j]
                packer = struct.Struct("BBB")
                pixel = packer.pack(r, g, b)
                socket.send(pixel)
           

    socket.send(b"end")
    reply = socket.recv(11)

    print  "server says : " + reply

def askcompress(connexion, nom):

    mess = "compress " + nom
    connexion.send(mess.encode('ascii'))
    reply = connexion.recv(2)
    print "server says : " + reply
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

    im.save("stor" + link, 'JPEG', quality = 100)



def askcoeff(conn, nom):

    unpacker = struct.Struct("bbbbbbbbb")

    print 'demande en cours'
    mess = "coef " + nom
    conn.send(mess.encode("ascii"))

    print "reception coefs"
    coefs = ''
    msg = ''
    while msg.endswith(b'end') == False:
        coefs += msg
        msg = conn.recv(9)
    print str(len(coefs)) + " octets recus"
    print "reconstitution image"
    image = Image.open("stor" + nom)
    pix = image.load()
    dim = image.size
    im =  Image.new("RGB", (dim[0] * 2, dim[1] * 2), "white" )
    px = im.load()
    for i in range(dim[0]):
        for j in range(dim[1]):
            tab = unpacker.unpack(coefs[(i*dim[1] + j)* unpacker.size : (i*dim[1] + j +1)* unpacker.size])
            
            px[2*i,2*j] = ( pix[i,j][0] + tab[0] + tab[3], pix[i,j][1] + tab[1] + tab[4], pix[i,j][2] + tab[2] + tab[5])
            px[2*i+1,2*j] = ( pix[i,j][0] + tab[0] - tab[3], pix[i,j][1] + tab[1] - tab[4], pix[i,j][2] + tab[2] - tab[5])
            px[2*i,2*j + 1] = ( pix[i,j][0] - tab[0] + tab[6], pix[i,j][1] - tab[1] + tab[7], pix[i,j][2] - tab[2] + tab[8])
            px[2*i+1,2*j+1] = ( pix[i,j][0] - tab[0] - tab[6], pix[i,j][1] - tab[1] - tab[7], pix[i,j][2] - tab[2] - tab[8])

            
    print "enregistrement"
    im.save('2' + nom, 'JPEG', quality = 100)
    conn.send(b'ok')


def main(arg):
    
    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if 'r' in arg[1]:
        try :
            connexion.connect((argv[3], 13337))
        except:
            connexion.connect(('srv.ordiclic.eu', 13337))
    else:
        connexion.connect(('localhost', 13337))

    if 's' in arg[1]:
        sendImage(connexion, arg[2])
        askcompress(connexion, 'srv' + arg[2])
        storeImage(arg[2])
    if 'd' in arg[1]:
        askcoeff(connexion, arg[2])
        
    connexion.send(b"stop")
    connexion.close()
    

if __name__ == "__main__":
    main(sys.argv)
