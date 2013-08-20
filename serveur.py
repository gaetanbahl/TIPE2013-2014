#-------------------------------------------------------------
# Name:        serveur.py
# Purpose:     serveur du TIPE sur les ondelettes
#
# Author:      Gaetan
#
# Created:     20/08/2013
# Copyright:   (c) Gaetan 2013
# Licence:     CC-BY-SA
#-------------------------------------------------------------


import socket
import Image
import time
import struct
import StringIO


def recvImage(conn,msg):
    title = msg.split(' ')
    image = Image.new("RGB", (int(title[1]),int(title[2])), "white" )
    pix = image.load()
    conn.send(b"ok")
    msg, img = "", ""
     
    while msg.endswith("end") == False:
        img += msg
        msg = conn.recv(4096)
        #msg = msg_recu.decode()
        
    print "pixels recus"
        
    #pixels = img.split(struct.pack("<c", ' '))
    for i in range(int(title[1])*int(title[2])):
        
        pixel = struct.unpack_from("<HHBBB",img,5)
        
        print pixel
        pix[int(pixel[0]), int(pixel[1])] = (int(pixel[2]), int(pixel[3]), int(pixel[4]))
        img = img[6:]
     
    print "image created"
    
    image.save("srv" + title[3], 'JPEG', quality = 100)
    print "image enregistree"
    conn.send(b'saved image')
  
                
def fasthaar_srv(socket, msg, epsilon=0):
    t = msg.split(' ')
    image = Image.open(t[1])
    pix = image.load()
    
    fichier = open(t[1] + "coef", 'wb')
    sizex,sizey = image.size
    
    txt = struct.pack("<HHc",sizex,sizey,"\n")
    fichier.write(txt)
    
    for x in range(sizex/2):

        for y in range(sizey/2):

            carres = []
            pixelscoef = str(x) + " " + str(y)
            
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
                if ondlmix[i] < epsilon:
                    pixelscoef += " 0"
                else:
                    pixelscoef += " " + str(ondlmix[i])

                if ondlhaut[i] < epsilon:
                    pixelscoef += " 0"
                else:
                    pixelscoef += " " + str(ondlhaut[i])

                if ondlbas[i] < epsilon:
                    pixelscoef += " 0"
                else:
                    pixelscoef += " " + str(ondlbas[i])
            t = pixelscoef.split(' ')           
            fichier.write(struct.pack("<BBBc",int(t[2]),int(t[3]),int(t[4])," "))
        fichier.write(struct.pack("<c",'\n'))
    
    fichier.close()
    print 'compression OK'
    socket.send(b"OK")

def main():
         
    hote = ''
    port = 13337

    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion.bind((hote, port))
    connexion.listen(5)
        
    msg_recu = b""
    connexion_client, infos_connexion = connexion.accept()

    print "client connected"
    
    while msg_recu != b"stop":
        time.sleep(0.1)
        msg = msg_recu.decode()
                
        if msg.startswith('sendimg'):
            print "image en cours de reception"
            recvImage(connexion_client, msg)
                
        if msg.startswith('compress'):
            print "compression en cours"
            fasthaar_srv(connexion_client, msg)
                  
        msg_recu = connexion_client.recv(1024)
                
               
               
 
    print("Exiting")
    connexion_client.close()
    connexion.close()

if __name__ == "__main__":
    main()
    
