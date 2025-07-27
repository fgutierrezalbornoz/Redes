import time
from utils import Packet, Window, WindowRcv
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
    global recv_seq, PACK_SZ, WINDOW_SIZE, MAX_SEQ, TIMEOUT
    window_rcv = WindowRcv(WINDOW_SIZE)
    eof = False
    s.settimeout(15)
    while not eof: #mientras no sea el eof
        try:
            data = s.recv(PACK_SZ) #se recibe la data
        except:
            data = None
        if not data:
            print("Rdr(): socket error!", file=sys.stderr)
            sys.exit(1)
        seq = from_seq(data[:HDR]) #se extrae el número de secuencia
        # print(seq, window.rtt, TIMEOUT)
        with window.cond: #condición de lock
            if window_rcv.in_window(seq): #si el paquete está dentro del rango esperado 
                if seq == window_rcv.base: #si es el primero de la ventana esperada
                    if len(data) == HDR:  # EOF
                        window.reset()
                        eof = True
                        break #aquí termina 
                    else:
                        window_rcv.store(seq, data[HDR:]) #se almacena el paquete llegado
                        window_rcv.write_in_order(fout) #se escribe en el archivo
                    expected_packet = window.data_indexed[seq] #el paquete esperado
                    recv_seq = seq #se actualiza la secuencia recibida
                    if not expected_packet.isRetransmitted: #si el paquete fue retransmitido no se considera en el RTT
                        rtt = time.time() - expected_packet.sending_date
                        window.calculate_rtt(rtt) #ahora no calcula promedio sino que considera el max
                        TIMEOUT = 2 * window.rtt
                    else:
                        # if (2 * window.rtt > TIMEOUT):
                        TIMEOUT = min(2, 2 * TIMEOUT) #se duplica el valor del timeout por si el RTT estuviera creciendo
                    expected_packet.isReceived = True #Marcamos como recibido para mover la ventana de envío
                    window.cond.notify() #se notifica a la ventana de envío para que siga enviando (unlock)
                else: #paquete dentro de la ventana esperada pero fuera de orden
                    if not window_rcv.received[seq] and len(data) > HDR: #si no ha sido marcado como recibido
                        window_rcv.store(seq, data[HDR:]) #se almacena
                        expected_packet = window.data_indexed[seq]
                        expected_packet.isReceived = True #se marca como recibido
            else: #si no está dentro de la ventana espeerada, no se toma en cuenta
                continue
    fout.close()

if len(sys.argv) != 8:
    print('Use: '+sys.argv[0]+' sz timeout win in out host port', file=sys.stderr)
    sys.exit(1)


PACK_SZ = int(sys.argv[1])
INITIAL_TIMEOUT = float(sys.argv[2])
TIMEOUT = INITIAL_TIMEOUT
WINDOW_SIZE = int(sys.argv[3])
path_file_in = sys.argv[4]
path_file_out = sys.argv[5]
fin = open(path_file_in, 'rb', 0)
fout = open(path_file_out, 'wb' )
s = jsockets.socket_udp_connect(sys.argv[6], sys.argv[7])
if s is None:
    print('could not open socket', file=sys.stderr)
    sys.exit(1)

window = Window(WINDOW_SIZE, 'sdr') #objeto ventana (del sender)
eof = False #flag para marcar el término de lectura

recv_thread = threading.Thread(target=Rdr, args=(s, fout, window))
recv_thread.start()
ti = time.time()

#sender
packs = 0
seq = 0
recv_seq = -1
retransmitted = 0
real_size = 0
cong_win_sz = WINDOW_SIZE
min_cong_win_sz = WINDOW_SIZE
can_reduce_cong_win = True
n = 0
cong_win_update = time.time()
while not (eof and window.is_empty()): #si la ventana no está vacía o no se ha llegado al final del archivo
    with window.cond:    
        n = window.slide() #corre la ventana
        # si la ventana de congestión tiene como flag que no se puede reducir,
        # pero ha pasado un RTT, la habilito para reducirla
        if not can_reduce_cong_win and (time.time() - cong_win_update) > window.rtt: 
            can_reduce_cong_win = True
        # si la ventana de envío se movió, y la ventana de congestión es más pequeña que la de envío
        # aumento el tamaño de la ventana de congestión en 1
        if n > 0 and cong_win_sz < window.real_size():
            cong_win_sz += 1
        #si la ventana está llena o si se alcanzó el tamaño de la ventana de congestión, 
        #calcula el próximo timeout de los paquetes no recibidos
        while window.is_full() or window.real_size() >= cong_win_sz: 
            now = time.time()
            tout = None
            for packet in window.get_packets():
                if not packet.isReceived: #si no se ha recibido, se recalcula el timeout
                    packet_timeout = packet.sending_date + TIMEOUT - now
                    if tout is None or packet_timeout < tout: #considera el menor
                        tout = packet_timeout
            if tout is None or tout < 0:
                tout = 0   
            if not window.cond.wait(tout): #si se cumple el timeout
                now = time.time()
                for packet in window.get_packets():
                    if not packet.isReceived and packet.sending_date + TIMEOUT < now: #solo se retransmiten los no recibidos
                        if can_reduce_cong_win:
                            cong_win_sz = max(1, round(cong_win_sz / 2))
                            min_cong_win_sz = min(cong_win_sz, min_cong_win_sz)
                            can_reduce_cong_win = False
                            cong_win_update = time.time()
                        hdr = to_seq(packet.packet_id)
                        s.send(hdr + packet.data_sent)
                        packet.retransmit() #se marca como retransmitido
                        retransmitted += 1 #se aumenta la cantidad de retransmisiones
                        # print('retransmitido', seq)
                n = window.slide() #se corre la ventana
                if not can_reduce_cong_win and (time.time() - cong_win_update) > window.rtt: 
                    can_reduce_cong_win = True

                if n > 0 and cong_win_sz < window.real_size():
                    cong_win_sz += 1
        #si no se ha terminado el archivo y se han enviado menos paquete de lo que la ventana de congesión permite
        if not eof and window.real_size() < cong_win_sz: 
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
        now = time.time()
        for packet in window.get_packets():
            if not packet.isReceived and packet.sending_date + TIMEOUT < now: #se vuelve a revisar si hay timeout para algún paquete
                if can_reduce_cong_win:
                    cong_win_sz = max(1, round(cong_win_sz / 2))
                    min_cong_win_sz = min(cong_win_sz, min_cong_win_sz)
                    can_reduce_cong_win = False
                    cong_win_update = time.time()
                hdr = to_seq(packet.packet_id)
                s.send(hdr + packet.data_sent)
                packet.retransmit()
                retransmitted += 1
        real_size = window.real_size() if window.real_size() > real_size else real_size #calculo del tamaño utilizado de la ventana
    

recv_thread.join()
s.close()

total_packets = packs + retransmitted
error = (retransmitted / total_packets) * 100 if total_packets > 0 else 0
total_time = time.time() - ti
bytes_sent = os.path.getsize(path_file_out)
bw = bytes_sent * 8 / (total_time * 1024 * 1024) # Mbits/sec
print("=============================================================")
if (sys.argv[6]=="127.0.0.1"):
    print(f"Test localhost size = {PACK_SZ}, timeout = {INITIAL_TIMEOUT}, window size = {WINDOW_SIZE}")
else:
    print(f"Test anakena size = {PACK_SZ}, timeout = {INITIAL_TIMEOUT}, window size = {WINDOW_SIZE}")
print(f"Total packets sent: {packs}")
print(f"Total packets transmitted (including retransmissions): {total_packets}")
print(f"Total error: {error:.2f}%")
print(f"Max size window : {real_size}")
print(f"Min size congestion window: {min_cong_win_sz}")
print(f"Estimated RTT : {window.rtt:.4f} sec")
print(f"Final variable timeout: {TIMEOUT:.4f} sec")
print(f"Bandwidth: {bw:.4f} Mbits/sec")