import time
import threading

MAX_SEQ = 1000
#Algunos métodos y campos implementados los usé inicialmente y puede que no se utilicen pero no los quise 
#borrar porque podría volver a utilizarlos.
class Packet:
    def __init__(self, packet_id, data_sent):
        self.packet_id = packet_id #aquí guardo el número de secuencia
        self.data_sent = data_sent #data contenida en el paquete
        self.data_received = None 
        self.sending_date = time.time() #tiempo cuando se envía
        self.isRetransmitted = False #sirve para saber si considerarlo en el cálculo de rtt
        self.isReceived = False #sirve para correr la ventana
        self.timeout = None
    
    def retransmit(self):
        self.sending_date = time.time()
        self.isRetransmitted = True

class Window:
    def __init__(self, size, window_name):
        self.window_name = window_name
        self.size = size #tamaño máximo de la ventana
        self.data = [] #contiene los objetos Packet que componen la ventana
        self.first = 0 #índice del inicio de la ventana (dejé de ocuparlo, debería mantenerse en cero)
        self.last = 0 
        self.cond = threading.Condition() #para hacer el lock del thread
        self.rtt = 0 #rtt estimado
        self.data_indexed = [None] * 1000 #para acceder más rápido a los paquetes

    def get_by_index(self, index):
        return self.data[index]
    
    def get_first(self):
        return self.data[self.first]
    
    def add(self, packet):
        if len(self.data) < self.size:
            self.data.append(packet)
            self.last = self.last + 1
            self.data_indexed[packet.packet_id] = packet
    
    def add_rcvr(self, packet):
        self.data.append(packet)
        self.data = self.data.sorted(self.data, key=lambda packet: packet.packet_id)
        self.data_indexed[packet.packet_id] = packet
        
    def reset(self):
        self.data = []
        self.first = 0
        self.last = 0

    def is_empty(self):
        return len(self.data) == 0
    
    def is_full(self):
        return len(self.data) == self.size
    
    def slide(self, write=False, fout=None):
        n = 0
        for packet in self.data:
            if packet.isReceived:
                if write and fout is not None:
                    fout.write(packet.data_sent)
                n += 1
            else:
                break
        if n > 0:
            self.data = self.data[n:]
            self.last -= n

    def get_packets(self):
        return self.data[self.first:self.last]
    
    def real_size(self):
        return len(self.data)
    
    def calculate_rtt(self, new_rtt):
        self.rtt = (self.rtt + new_rtt) / 2

    def between(self, seq, base, max_seq=MAX_SEQ):
        size = self.size
        max_win = (base + size) % max_seq
        if base <= max_win:
            return base <= seq < max_win
        else:
            return base <= seq or seq < max_win
    
    def status(self):
        def is_received(packet):
            if packet is None: return None
            return packet.packet_id
        return list(map(is_received, self.data))

class WindowRcv(Window):
        def __init__(self, size):
            self.size = size
            self.base = 0 #marca el inicio de la ventana rcv
            self.data_buffer = [None] * MAX_SEQ #sirve para lograr ordenar los paquetes recibidos
            self.received = [False] * MAX_SEQ #flag para marcar paquetes recibidos

        def in_window(self, seq):
            max_win = (self.base + self.size) % MAX_SEQ
            if self.base <= max_win:
                return self.base <= seq < max_win
            else:
                return seq >= self.base or seq < max_win

        def store(self, seq, data):
            self.data_buffer[seq] = data
            self.received[seq] = True

        def write_in_order(self, fout):
            while self.received[self.base] and self.data_buffer[self.base] is not None: #Esto simula correr la ventana de recepción
                fout.write(self.data_buffer[self.base])
                self.data_buffer[self.base] = None
                self.received[self.base] = False
                self.base = (self.base + 1) % MAX_SEQ
