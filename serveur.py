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



def recvImage(socket,msg):
    title = msg.split(' ')
    image = Image.new("RGB", (int(title[1]),int(title[2])), "white" )
    pix = image.load()
    socket.send(b"ok")
    blbl = socket.recv(2)
    while blbl != b"en":
                
        msg_recu = socket.recv(int(blbl.decode()))
        msg = msg_recu.decode()
        pixel = msg.split()
        print blbl
        print pixel
        pix[int(pixel[0]), int(pixel[1])] = (int(pixel[2]), int(pixel[3]), int(pixel[4]))
        blbl = socket.recv(2)
                
    image.save("srv" + title[3], 'JPEG', quality = 100)
    socket.send(b'saved image')
                
def fasthaar_srv(socket, msg, epsilon):
    t = msg.split(' ')
    image = Image.open(t[1])
    pix = image.load()
    
    file = open(t[1] + "coef", 'w')


    for x in range(xa / 2, xb / 2):

        for y in range(ya / 2, yb / 2):

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
                carres[i][0][0] = (carres[i][0][0] + carres[i][0][1]) / 2

            for i in range(3):
                if ondlmix[i] < epsilon:
                    carres[i][0][1] = carres[i][0][0]
                else:
                    carres[i][0][1] = carres[i][0][0] - ondlmix[i]
                    carres[i][0][0] = carres[i][0][0] + ondlmix[i]

                if ondlhaut[i] < epsilon:
                    carres[i][1][0] = carres[i][0][0]
                else:
                    carres[i][1][0] = carres[i][0][0] - ondlhaut[i]
                    carres[i][0][0] = carres[i][0][0] + ondlhaut[i]

                if ondlbas[i] < epsilon:
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
         
    hote = ''
    port = 13337

    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion.bind((hote, port))
    connexion.listen(5)
        
    msg_recu = b""
    connexion_client, infos_connexion = connexion.accept()

        
    while msg_recu != b"stop":
                
        msg = msg_recu.decode()
        print msg
                
        if msg.startswith('sendimg'):
            recvImage(connexion_client, msg)
                
        if msg.startswith('compress')
            fasthaar_srv(connexion_client, msg)
                  
        msg_recu = connexion_client.recv(1024)
                
               
               
 
    print("Exiting")
    connexion_client.close()
    connexion.close()

if __name__ == "__main__":
    main()
    
