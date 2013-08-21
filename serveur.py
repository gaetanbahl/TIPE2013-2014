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



def recvImage(conn,msg):
    title = msg.split(' ')
    sizex,sizey = int(title[1]),int(title[2])
    image = Image.new("RGB", (sizex,sizey), "white" )
    pix = image.load()
    conn.send(b"ok")
    msg, img = "", ""
    unpacker = struct.Struct("BBB")
    while msg.endswith("end") == False:
        img += msg
        msg = conn.recv(65536)


    print "pixels recus"

    for i in range(sizex):
        for j in range(sizey):
            pixel = unpacker.unpack(img[(i*sizey + j)*unpacker.size:(i*sizey + j + 1)*unpacker.size])

            pix[i, j] = (int(pixel[0]), int(pixel[1]), int(pixel[2]))
        print i

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

    txt = struct.pack("HH",sizex,sizey)
    fichier.write(txt)
    print "compression en cours"
    for x in range(sizex/2):
        for y in range(sizey/2):

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
                if ondlmix[i] < epsilon:
                    ondlmix[i] = 0
                if ondlhaut[i] < epsilon:
                    ondlhaut[i] = 0
                if ondlbas[i] < epsilon:
                    ondlbas[i] = 0
				fichier.write(struct.pack("BBB",ondlmix[i],ondlhaut[i],ondlbas[i]))


    fichier.close()
    print 'compression OK'
    socket.send(b"OK")


def sendCoef(sock, msg):
	banana = msg.split(" ")
	fichier = open(banana[1] + "coef", 'rb')
	print "envoi des coefficients"






def main():

    hote = ''
    port = 13337

    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion.bind((hote, port))
	while 1:
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

				fasthaar_srv(connexion_client, msg)

			if msg.startswith('coef'):

				sendCoef(connexion_client, msg)


			msg_recu = connexion_client.recv(1024)




    print("Exiting")
    connexion_client.close()
    connexion.close()

if __name__ == "__main__":
    main()

