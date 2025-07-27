#!/usr/bin/python3
# Echo client program
# Version con dos threads: uno lee de stdin hacia el socket y el otro al revés
import jsockets, socket
import sys, threading
import time


bytesSent = 0
def Sdr(s, fileToSend, size):
    global bytesSent
    B = size
    with open(fileToSend, "rb") as file:
        while True:
            line = file.read(B)
            if not line: # EOF
                s.send(b"")
                s.settimeout(3)
                break
            try:
                s.send(line)
                bytesSent += len(line) 
            except: 
                print('No se pudo enviar la información')
                break
    with open("sentBytes.txt", "a") as fileB:
        fileB.write(str(bytesSent)+"\n")

def Rdr(s, fileToReceive, sizeRW):
    sizeReceived = 0
    with open(fileToReceive, "wb") as file:
        while True:
            try:
                data = s.recv(sizeRW)
                if not data:
                    # with open("receivedBytes.txt", "a") as fileB:
                    #     fileB.write(str(sizeReceived)+"\n")
                    break
                file.write(data)
                sizeReceived+=len(data)
            except TimeoutError:
                print('Se agotó el tiempo de espera')
                with open("receivedBytes.txt", "a") as fileB:
                        fileB.write("Medición no válida ")
                break
    with open("receivedBytes.txt", "a") as fileB:
        fileB.write(str(sizeReceived)+"\n")
    
    s.close()

if len(sys.argv) != 6:
    print('Use: '+sys.argv[0]+' size IN OUT host port')
    sys.exit(1)

size = int(sys.argv[1])
inFile = sys.argv[2]
outFile = sys.argv[3]
host = sys.argv[4]
port = sys.argv[5]

s = jsockets.socket_udp_connect(host, port)

if s is None:
    print('could not open socket')
    sys.exit(1)

# Esto es para dejar tiempo al server para conectar el socket
s.send(b'hola')
s.recv(1024)


# Primero, crea los threads
send_thread = threading.Thread(target=Sdr, args=(s, inFile, size))
recv_thread = threading.Thread(target=Rdr, args=(s, outFile, size))

# Inicia ambos
send_thread.start()
recv_thread.start()

# Espera que ambos terminen
send_thread.join()
recv_thread.join()