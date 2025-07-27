#!/usr/bin/python3
# Echo client program
# Version con dos threads: uno lee de stdin hacia el socket y el otro al revés
import jsockets
import sys, threading

bytesSent = 0
def Sdr(s, fileToSend, size):
    global bytesSent
    B = size
    with open(fileToSend, "rb") as file:
        while True:
            line = file.read(B)
            if not line: # EOF
                break
            try:
                s.send(line)
                bytesSent += len(line) 
            except: 
                print('No se pudo enviar la información')
                break
    with open("sentBytes.txt", "a") as fileB:
        fileB.write(str(bytesSent)+"\n")
    #print(f'Se enviaron {bytesSent} bytes al servidor')

def Rdr(s, fileToReceive, sizeRW, sizeToReceive):
    sizeReceived = 0
    with open(fileToReceive, "wb") as file:
        while sizeReceived < sizeToReceive:
            try:
                data = s.recv(sizeRW)
                if not data: 
                    print('no hay data que leer')
                    break
                file.write(data)
                sizeReceived+=len(data)
            except:
                print('Error al recibir los datos')
                break
    with open("receivedBytes.txt", "a") as fileB:
        fileB.write(str(sizeReceived)+"\n")
    s.close()
    #print(f'Se recibieron {sizeReceived/sizeToReceive*100}% de los datos enviados')


clientFile = sys.argv[0]
if len(sys.argv) != 6:
    print('Use: '+ clientFile +' size in out host port')
    sys.exit(1)


size = int(sys.argv[1])
inFile = sys.argv[2]
outFile = sys.argv[3]
host = sys.argv[4]
port = sys.argv[5]

s = jsockets.socket_tcp_connect(host, port)
if s is None:
    print('could not open socket')
    sys.exit(1)

Sdr(s, inFile, size)
# Creo thread que lee desde el socket hacia stdout:
newthread = threading.Thread(target=Rdr, args=(s,outFile,size,bytesSent,))
newthread.start()

newthread.join()






