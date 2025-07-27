import time, subprocess, os, threading
import shutil


def runClient(size, inFile, outFile, host):
    client = subprocess.Popen(
        ["python3", "client_echo_udp3.py", str(size), inFile, outFile, host, "1818"]
    )
    #print('Enviando datos al servidor...')
    time.sleep(5)
    #print('Finalizando proceso del cliente')
    client.terminate()
    client.wait()

def runThreadClient(size, nThr, ini):
    size=str(size)
    threads = []
    inFile = "archivo10KB.bin"
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
size=10000
print(f"================ Experimento 1: Enviando un archivo de 500KB a Anakena con size={size} bytes ================")
hora_actual = time.strftime("%H:%M", time.localtime())
print(f"Hora experimento: {hora_actual}")
os.makedirs("./experimento1", exist_ok=True)
start_time = time.time()
runClient(str(size), "archivo500KB.bin", "experimento1/salida_E1A.txt", "anakena.dcc.uchile.cl")
total_time = time.time() - start_time - 5 #5 segundo para terminar en runClient
#Cálculo del ancho de banda
with open("sentBytes.txt", "r") as fileB:
    sentBytes = int(fileB.readline())
try:
    with open("receivedBytes.txt", "r") as fileB:
        receivedBytes = int(fileB.readline())
        # data = fileB.readline()
        # if not data == "Medición no válida":
        #     sentBytes = int(data)
    bw = (sentBytes + receivedBytes)*10//(1000 * 1000 * total_time)/10
    lost = int((1 - receivedBytes/sentBytes) * 1000) / 10
    print(f"Se enviaron {sentBytes} bytes y se recibieron {receivedBytes} bytes")
    print(f"Se perdió el {lost}% de los datos.")
    print(f"Ancho de banda = {bw} MB/s")
except:
    print("Medición no válida")
print(f"================ Fin del experimento ================")



sizeThr = size #size
nThr = 20 #número de threads
print(f"================ Experimento 2: Enviando {4*nThr} archivos de 10KB a Anakena con size={size}bytes ================")
hora_actual = time.strftime("%H:%M", time.localtime())
print(f"Hora experimento: {hora_actual}")
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
total_time_th = time.time() - start_time_th - 5
sentBytesThr = 0
receivedBytesThr = 0

#Cálculo del ancho de banda para el experimento 2
with open("sentBytes.txt", "r") as fileS:
    lineasS = fileS.readlines()
try:
    with open("receivedBytes.txt", "r") as fileR:
        lineasR = fileR.readlines()
    listaBytesSent = lineasS[1:]
    listaBytesReceived = lineasR[1:]
    for i in range(len(listaBytesReceived)):
        lineR = listaBytesReceived[i]
        if lineR and lineR[0].isdigit():
            receivedBytesThr += int(lineR.strip())
            sentBytesThr += int(listaBytesSent[i])
    bw = (sentBytes + receivedBytes)*10//(1000 * 1000 * total_time)/10
    lost = int((1 - receivedBytes/sentBytes) * 1000) / 10
    bwTh = (sentBytesThr + receivedBytesThr)*10//(1000 * total_time_th)/10

    lostThr = int((1 - receivedBytesThr/sentBytesThr) * 1000) / 10
    
    print(f"Se enviaron {sentBytesThr} bytes y se recibieron {receivedBytesThr} bytes")
    print(f"Se perdió el {lostThr}% de los datos.")
    print(f"Ancho de banda = {bwTh} KB/s")
except:
    print("Medición no válida")
print(f"================ Fin del experimento ================")






# print(f"================ Experimento 1: Enviando un archivo de 600MB en localhost con size={size} bytes ================")
# hora_actual = time.strftime("%H:%M", time.localtime())
# print(f"Hora experimento: {hora_actual}")
# os.makedirs("./experimento1", exist_ok=True)
# start_time = time.time()
# runClient(str(size), "archivo600MB.bin", "experimento1/salida_E1L.txt", "127.0.0.1") # prueba con size = 1000
# total_time = time.time() - start_time - 3 #3 segundo para terminar en runClient
# #Cálculo del ancho de banda
# with open("sentBytes.txt", "r") as fileB:
#     sentBytes = int(fileB.readline())
# try:
#     with open("receivedBytes.txt", "r") as fileB:
#         receivedBytes = int(fileB.readline())
#         # data = fileB.readline()
#         # if not data == "Medición no válida":
#         #     sentBytes = int(data)
#     bw = (sentBytes + receivedBytes)*10//(1000 * 1000 * total_time)/10
#     lost = int((1 - receivedBytes/sentBytes) * 1000) / 10
#     print(f"Se enviaron {sentBytes} bytes y se recibieron {receivedBytes} bytes")
#     print(f"Se perdió el {lost}% de los datos.")
#     print(f"Ancho de banda = {bw} MB/s")
# except:
#     print("Medición no válida")


# Limpieza archivos generados
pathExp1 = "experimento1"
pathExp2 = f"experimento2_{size}"
if os.path.exists(pathExp1):
    shutil.rmtree(pathExp1)


if os.path.exists(pathExp2):
    shutil.rmtree(pathExp2)