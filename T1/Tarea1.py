import time, subprocess, os, threading


def runClient(size, inFile, outFile, host):
    client = subprocess.Popen(
        ["python3", "client_tarea.py", str(size), inFile, outFile, host, "1818"]
    )
    #print('Enviando datos al servidor...')
    time.sleep(3)
    #print('Finalizando proceso del cliente')
    client.terminate()
    client.wait()

def runThreadClient(size, nThr, ini):
    size=str(size)
    threads = []
    inFile = "archivo5KB.txt"
    os.makedirs(f"./experimento2_{size}", exist_ok=True)
    for i in range(ini, ini + nThr):
        newthread = threading.Thread(target=runClient, args=(size,inFile,f"experimento2_{size}/salida{i}_E2.txt","anakena.dcc.uchile.cl",))
        newthread.start()
        threads.append(newthread)
    for t in threads:
        t.join()


#reseto de bytes del experimento en una iteración anterior
if os.path.exists("sentBytes.txt"):
    os.remove("sentBytes.txt")
else:
    with open("sentBytes.txt", "w") as file:
        pass 
if os.path.exists("receivedBytes.txt"):
    os.remove("receivedBytes.txt")
else:
    with open("receivedBytes.txt", "w") as file:
        pass 
size=4000
print(f"================ Experimento 1: Enviando un archivo de 500KB a Anakena con size={size} bytes ================")
os.makedirs("./experimento1", exist_ok=True)
start_time = time.time()
runClient(str(size), "archivo500KB.txt", "experimento1/salida_E1.txt", "anakena.dcc.uchile.cl") # prueba con size = 1000
total_time = time.time() - start_time - 3 #3 segundos para terminar en runClient
#Cálculo del ancho de banda
with open("sentBytes.txt", "r") as fileB:
    sentBytes = int(fileB.readline())
with open("receivedBytes.txt", "r") as fileB:
    receivedBytes = int(fileB.readline())  


bw = (sentBytes + receivedBytes)*10//(1000 * 1000 * total_time)/10
print(f"Se enviaron {sentBytes} bytes y se recibieron {receivedBytes} bytes")
print(f"Ancho de banda = {bw} MB/s")

sizeThr = size #size
nThr = 20 #número de threads
print(f"================ Experimento 2: Enviando {4*nThr} archivos de 5KB a Anakena con size={size}bytes ================")

start_time_th = time.time()
runThreadClient(sizeThr, nThr, 0)
nt2 = threading.Thread(target=runThreadClient, args=(sizeThr, nThr, nThr))
nt3 = threading.Thread(target=runThreadClient, args=(sizeThr, nThr, 2*nThr))
nt4 = threading.Thread(target=runThreadClient, args=(sizeThr, nThr, 3*nThr))

#paralelo
nt2.start()
nt3.start()
nt4.start()
nt2.join()
nt3.join()
nt4.join()
total_time_th = time.time() - start_time_th - 3
sentBytesThr = 0
receivedBytesThr = 0

#Cálculo del ancho de banda para el experimento 2
with open("sentBytes.txt", "r") as fileS:
    lineasS = fileS.readlines()

with open("receivedBytes.txt", "r") as fileR:
    lineasR = fileR.readlines()

listaBytesSent = lineasS[1:]
listaBytesReceived = lineasS[1:]

for line in listaBytesSent:
    sentBytesThr+=int(line.strip())

for line in listaBytesReceived:
    receivedBytesThr+=int(line.strip())

bwTh = (sentBytesThr + receivedBytesThr)*10//(1000 * total_time_th)/10

print(f"Se enviaron {sentBytesThr} bytes y se recibieron {receivedBytesThr} bytes")
print(f"Ancho de banda = {bwTh} KB/s")
