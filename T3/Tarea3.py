import time, subprocess, os
import shutil


def runClient(size, timeout, inFile, outFile, host):
    subprocess.run(
        ["python3", "client_t3.py", str(size), str(timeout), inFile, outFile, host, "1818"]
    )



#reseto de bytes del experimento en una iteración anterior
if os.path.exists("sentBytes.txt"):
    os.remove("sentBytes.txt")

with open("sentBytes.txt", "w") as file:
    pass 
if os.path.exists("receivedBytes.txt"):
    os.remove("receivedBytes.txt")

with open("receivedBytes.txt", "w") as file:
    pass 
if os.path.exists("sentPackets.txt"):
    os.remove("sentPackets.txt")

with open("sentPackets.txt", "w") as file:
    pass 
size=2000
timeout=0.04#0.05
print(f"================ Experimento 1: Enviando un archivo de 500KB a Anakena con size={size} bytes y timeout={timeout} seg================")
hora_actual = time.strftime("%H:%M", time.localtime())
print(f"Hora experimento: {hora_actual}")
os.makedirs("./experimento1", exist_ok=True)
start_time = time.time()
runClient(str(size), timeout,"archivo500KB.bin", "experimento1/salida_E1A.txt", "anakena.dcc.uchile.cl")
total_time = time.time() - start_time
# Cálculo del ancho de banda
with open("sentBytes.txt", "r") as fileB:
    sentBytes = int(fileB.readline())
with open("sentPackets.txt", "r") as fileP:
    sentPackline = fileP.readline()
    sentPack, n_err, n_err_eof = sentPackline.split('###')
    sentPack = int(sentPack)
    n_err = int(n_err)
    n_err_eof = int(n_err_eof)
try:
    with open("receivedBytes.txt", "r") as fileB:
        receivedBytes = int(fileB.readline())
    #resultados del experimento
    lost = int((n_err/sentPack) * 1000) / 10
    lost_wo_eof = int((n_err - n_err_eof) /(sentPack - n_err_eof) * 1000) / 10
    print(f"Se enviaron {sentBytes} bytes y se recibieron {receivedBytes} bytes")
    print(f"Se enviaron {sentPack} paquetes y se perdieron {n_err} paquetes")
    print(f"Se perdió el {lost}% de los paquetes.")
    print(f"Del total de los paquetes perdidos, {n_err_eof} están relacionado con el eof enviado.")
    print(f"Esto corresponde al {int((n_err_eof/n_err) * 1000) / 10}% del total de los paquetes perdidos.")
    print(f"Si no consideramos los paquetes perdidos por el EOF, se tiene que se perdió el {lost_wo_eof}% de los paquetes.")
    bw = (sentBytes + receivedBytes) / (1000 * total_time) 
    bw = round(bw, 1)
    print(f"Ancho de banda = {bw} KB/s")
except:
    print("Medición no válida")
print(f"================ Fin del experimento ================")

# Limpieza archivos generados
pathExp1 = "experimento1"
archivos = [f for f in os.listdir(pathExp1) if os.path.isfile(os.path.join(pathExp1, f))]
for archivo in archivos:
    open_file = open(pathExp1+'/'+archivo) 
    open_file.close()
if os.path.exists(pathExp1):
    shutil.rmtree(pathExp1)