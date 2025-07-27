import time
from utils import Packet, Window
import sys
import jsockets
import threading
import os

PACK_SZ=1500
MAX_SEQ = 1000
HDR = 3 # 000-999

def to_seq(n):
    if n < 0 or n > 999:
        print("invalid seq", file=sys.stderr)
        sys.exit(1)
    return format(n,'03d').encode()

def from_seq(s):
    return int(s.decode())

def Rdr(s, fout, window):
    global recv_seq, PACK_SZ
    expected_seq = 0
    s.settimeout(15) #timeout de 15 seg al socket
    while True:
        try:
            data = s.recv(PACK_SZ) 
        except:
            data = None
        if not data:
            print("Rdr(): socket error!", file=sys.stderr)
            sys.exit(1)

        seq = from_seq(data[:HDR]) 
        with window.cond:
            expected_packet = window.data_indexed[seq] #paquete esperado
            if seq == expected_seq: #si el que llegó es el que esperaba
                recv_seq = seq #actualizo el último recibido
                expected_seq = (expected_seq+1)%MAX_SEQ #actualizo la seq esperada
                if not expected_packet.isRetransmitted: #si el paquete no fue retransmitido 
                    rtt = time.time() - expected_packet.sending_date #calculo el nuevo rtt
                    window.calculate_rtt(rtt) #actualiza el rtt estimado
                expected_packet.isReceived = True #marco como recibido el paquete
                window.cond.notify() #notifico para que se sigan enviando paquetes
        if len(data) == HDR:  # EOF
            window.reset()
            break

        fout.write(data[HDR:])

    fout.close()

if len(sys.argv) != 8:
    print('Use: '+sys.argv[0]+' sz timeout win in out host port', file=sys.stderr)
    sys.exit(1)


PACK_SZ = int(sys.argv[1])
TIMEOUT = float(sys.argv[2])
WINDOW_SIZE = int(sys.argv[3])
path_file_in = sys.argv[4]
path_file_out = sys.argv[5]
fin = open(path_file_in, 'rb', 0)
fout = open(path_file_out, 'wb' )
s = jsockets.socket_udp_connect(sys.argv[6], sys.argv[7])
if s is None:
    print('could not open socket', file=sys.stderr)
    sys.exit(1)

window = Window(WINDOW_SIZE) #objeto ventana
eof = False #flag para marcar el término de lectura

recv_thread = threading.Thread(target=Rdr, args=(s, fout, window))
recv_thread.start()
ti = time.time()

#sender
packs = 0
errs = 0 
seq = 0
recv_seq = -1
retransmitted = 0
real_size = 0
while not (eof and window.is_empty()): #si la ventana no está vacía o no se ha llegado al final del archivo
    window.slide() #corre la ventana
    while window.is_full(): #si la ventana está llena
        tout = window.get_first().sending_date + TIMEOUT - time.time() # actualizamos timeout
        if tout < 0:
            tout = 0
        with window.cond:    
            if not window.cond.wait(tout): #si se cumple el timeout
                errs += 1
                for packet in window.get_packets(): # se retransmite la ventana
                    hdr = to_seq(packet.packet_id)
                    s.send(hdr + packet.data_sent)
                    packet.retransmit() #se marca como retransmitido
                    retransmitted += 1 #se aumenta la cantidad de retransmisiones
            window.slide() #se corre la ventana
    if not eof: #si no se ha terminado el archivo
        data = fin.read(PACK_SZ-HDR)
        hdr = to_seq(seq)
        if not data: #si ya se terminó de leer el archivo
            eof = True #se marca como finalizada la lectura
            window.add(Packet(seq, b'')) #se agrega el paquete a la ventana
            s.send(hdr + b'') #se envia el paquete
        else: #si queda archivo por leer
            window.add(Packet(seq, data))
            s.send(hdr + data)
            packs += 1
        seq = (seq + 1) % MAX_SEQ
    if not window.is_empty(): #si la ventana no está vacía
        if window.get_first().sending_date + TIMEOUT < time.time(): #se verifica el timeout
            errs += 1
            for packet in window.get_packets(): #se retransmite
                hdr = to_seq(packet.packet_id)
                s.send(hdr + packet.data_sent)
                packet.retransmit()
                retransmitted += 1
    real_size = window.real_size() if window.real_size() > real_size else real_size #calculo del tamaño utilizado de la ventana
    

recv_thread.join()
s.close()

total_packets = packs + retransmitted
error_percentage = (errs / packs) * 100 if packs > 0 else 0
extra_percentage = (retransmitted / packs) * 100 if packs > 0 else 0
total_time = time.time() - ti
bytes_sent = os.path.getsize(path_file_out)
bw = bytes_sent * 8 / (total_time * 1024 * 1024) # Mbits/sec
print("=============================================================")
if (sys.argv[6]=="127.0.0.1"):
    print(f"Test localhost size = {PACK_SZ}, timeout = {TIMEOUT}, window size = {WINDOW_SIZE}")
else:
    print(f"Test anakena size = {PACK_SZ}, timeout = {TIMEOUT}, window size = {WINDOW_SIZE}")
print(f"Total packets sent: {packs}")
print(f"Total errors (windows retransmitted): {errs}")
print(f"Error percentage: {error_percentage:.2f}%")
print(f"Total packets transmitted (including retransmissions): {total_packets}")
print(f"Extra packets transmitted due to retransmissions: {extra_percentage:.2f}%")
print(f"Max size window : {real_size}")
print(f"Estimated RTT : {window.rtt:.4f} sec")
print(f"Bandwidth: {bw:.4f} Mbits/sec")