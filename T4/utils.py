import time
import threading

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
    
    def retransmit(self):
        self.sending_date = time.time()
        self.isRetransmitted = True

class Window:
    def __init__(self, size):
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
    def reset(self):
        self.data = []
        self.first = 0
        self.last = 0

    def is_empty(self):
        return len(self.data) == 0
    
    def is_full(self):
        return len(self.data) == self.size
    
    def slide(self):
        for packet in self.data:
            if packet.isReceived:
                self.data.remove(packet)
                self.first = 0
                self.last -= 1
            else:
                break

            # self.data = self.data[n:]
            # self.first = 0#(self.first + n) % self.size
            # self.last -= n

    def get_packets(self):
        return self.data[self.first:self.last]
    
    def real_size(self):
        return len(self.data)
    
    def calculate_rtt(self, new_rtt):
        self.rtt = (self.rtt + new_rtt) / 2