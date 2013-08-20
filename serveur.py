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



def recvImage(conn,msg):
    title = msg.split(' ')
    image = Image.new("RGB", (int(title[1]),int(title[2])), "white" )
    pix = image.load()
    conn.send(b"ok")
    blbl = conn.recv(2)
    while blbl != b"en":
                
        msg_recu = conn.recv(int(blbl.decode()))
        msg = msg_recu.decode()
        pixel = msg.split()
        print blbl
        print msg
        pix[int(pixel[0]), int(pixel[1])] = (int(pixel[2]), int(pixel[3]), int(pixel[4]))
        #conn.send(b"ok")
        blbl = conn.recv(2)
                
    image.save("srv" + title[3], 'JPEG', quality = 100)
    conn.send(b'saved image')
                
def fasthaar_srv(socket, msg, epsilon=0):
    t = msg.split(' ')
    image = Image.open(t[1])
    pix = image.load()
    
    file = open(t[1] + "coef", 'wb')
    sizex,sizey = image.size

    file.write(str(sizex) + " " + str(sizey) + " \n")
    
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
                    pixelscoef += ",0"
                else:
                    pixelscoef += "," + str(ondlhaut[i])

                if ondlbas[i] < epsilon:
                    pixelscoef += ",0"
                else:
                    pixelscoef += "," + str(ondlbas[i])

            file.write(pixelscoef + " \n")


    file.close()
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

        
    while msg_recu != b"stop":
                
        msg = msg_recu.decode()
                
        if msg.startswith('sendimg'):
            recvImage(connexion_client, msg)
                
        if msg.startswith('compress'):
            fasthaar_srv(connexion_client, msg)
                  
        msg_recu = connexion_client.recv(1024)
                
               
               
 
    print("Exiting")
    connexion_client.close()
    connexion.close()

if __name__ == "__main__":
    main()
    
