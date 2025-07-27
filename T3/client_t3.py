#!/usr/bin/python3
# Echo client program
# Version con dos threads: uno lee de stdin hacia el socket y el otro al revés
import jsockets, socket
import sys, threading
import time

received = threading.Event() #variable compartida que indica envío/recibo de la data
received.set()
bytesSent = 0
received_eof = threading.Event()
def Sdr(s, fileToSend, size, timeout):
    global bytesSent, received, received_eof
    B = size
    nsec = -1 #n° de secuencia
    err = 0 #n° de retransmisiones
    n_pack = 0 #n° de paquetes totales
    err_eof = 0 #n° de retransmisiones del eof
    settimeout_flag = False #flag para el timeout de cierre de socket
    with open(fileToSend, "rb") as file:
        while True:
            if received.is_set(): #si se recibió la data se lee el siguiente paquete
                line = file.read(B)
                nsec = (nsec + 1)%1000
                nsec_format = str(nsec).zfill(3)
            try:
                if not line:  # EOF
                    if received_eof.is_set() : #ya se envió el eof y se recibió
                        break
                    final_msg = nsec_format.encode()
                    s.send(final_msg)
                    received.clear()
                    if not settimeout_flag:
                        s.settimeout(3)
                        settimeout_flag = True
                    received.wait(timeout)

                else: #data no EOF
                    s.send(nsec_format.encode() + line)
                n_pack += 1
                received.clear()

                bytesSent += len(line) #bytes enviados
                if not received.wait(timeout):
                    err += 1
                    if not line:
                        err_eof +=1
            except OSError as e: #utilizado en debugging
                if e.errno == 9:  # Bad file descriptor
                    print("Socket ya está cerrado.")
                else:
                    print("Se tuvo otro error", e)
                break
    with open("sentBytes.txt", "a") as fileB:
        fileB.write(str(bytesSent)+"\n")
    with open("sentPackets.txt", "a") as fileP:
        fileP.write(str(n_pack)+'###'+str(err)+'###'+str(err_eof)+"\n")

def Rdr(s, fileToReceive, sizeRW):
    global received, received_eof
    sizeReceived = 0
    nsec = -1 #n° de secuencia recibido
    with open(fileToReceive, "wb") as file:
        while True:
            try:
                data_received = s.recv(sizeRW) #n°secuencia + data
                nsec_received = int(data_received[:3].decode())
                data = data_received[3:]
                if not data: #se recibe el eof
                    received_eof.set()
                    break
                #se descartan los paquetes que ya llegaron pero solo se verifica con respecto al último que llegó
                if (nsec + 1) % 1000 == nsec_received: 
                    file.write(data)
                    sizeReceived+=len(data)
                    nsec = nsec_received
                    received.set()
            except TimeoutError:
                print('Se agotó el tiempo de espera')
                with open("receivedBytes.txt", "a") as fileB:
                        fileB.write("Medición no válida ")
                break
    with open("receivedBytes.txt", "a") as fileB:
        fileB.write(str(sizeReceived)+"\n")
    s.close()

if len(sys.argv) != 7:
    print('Use: '+sys.argv[0]+' size IN OUT host port')
    sys.exit(1)

size = int(sys.argv[1])
timeout = float(sys.argv[2])
inFile = sys.argv[3]
outFile = sys.argv[4]
host = sys.argv[5]
port = sys.argv[6]

s = jsockets.socket_udp_connect(host, port)

if s is None:
    print('could not open socket')
    sys.exit(1)

# Esto es para dejar tiempo al server para conectar el socket
s.send(b'hola')
s.recv(1024)


# Primero, crea los threads
send_thread = threading.Thread(target=Sdr, args=(s, inFile, size, timeout))
recv_thread = threading.Thread(target=Rdr, args=(s, outFile, size))

# Inicia ambos
send_thread.start()
recv_thread.start()

# Espera que ambos terminen
send_thread.join()
recv_thread.join()

