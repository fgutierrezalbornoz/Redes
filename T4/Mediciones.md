# Tarea 4: Cliente eco UDP con Go-Back-N para medir performance
Los archivos utilizados en esta tarea son:
- `client_gbn.py` donde se configura el cliente.
- `utils.py` donde se definen las clases packet y window utilizadas para implementar el protocolo gbn.
- `jsockets.py` archivo que se importa en el script del cliente.
- `archivo500KB.bin` archivo de entrada para el experimento. 
- `archivo600MB.bin` archivo de entrada para el experimento en localhost (no se incluye). 
- `logAnakena.bin` archivo que contiene los resultados de los experimentos con host anakena.
- `logLocal.bin` archivo que contiene los resultados de los experimentos con local host.

## Implementación 
En `client_gbn.py` se encuentran definidas las funciones para comunicarse con un servidor vía sockets mediante el protocolo UDP implementando go-back-n. En el script `utils.py` se definen las clases Window y Packet que se utiliza en la implementación del protocolo. La implementación del sender fue siguiendo el pseudo código del enunciado de la tarea y el reader siguiendo la base subida por el profe a material docente.
## Mediciones
Para medir el ancho de banda (wb) se realizaron experimentos que usa `client_gbn.py`. Los servidores utilizados fueron anakena.dcc.uchile.cl y localhost.

Con anakena se probó con dos size (1400 y 4000) y en localhost con size = 10000 inspeccionando tamaños de ventana de 1 hasta 1000 y con un timeout de 0.1.

### Anakena
$size = 1400$
| Window Size | Packets Sent | Errors | Error % | Total Transmitted | Retransmissions % | Max Window | RTT (sec) | Bandwidth (Mbit/s) |
|-------------|---------------|--------|---------|--------------------|--------------------|-------------|------------|---------------------|
| 1           | 371           | 0      | 0.00%   | 371                | 0.00%              | 1           | 0.0147     | 0.8283              |
| 10          | 371           | 2      | 0.54%   | 384                | 3.50%              | 10          | 0.0773     | 5.0400              |
| 15          | 371           | 0      | 0.00%   | 371                | 0.00%              | 15          | 0.0660     | 10.3402             |
| 20          | 371           | 2      | 0.54%   | 402                | 8.36%              | 20          | 0.0958     | 9.7453              |
| 50          | 371           | 3      | 0.81%   | 438                | 18.06%             | 50          | 0.0811     | 5.2377              |
| 80          | 371           | 1      | 0.27%   | 392                | 5.66%              | 80          | 0.0947     | 9.5982              |
| 100         | 371           | 3      | 0.81%   | 620                | 67.12%             | 100         | 0.0559     | 12.5920             |
| 150         | 371           | 8      | 2.16%   | 1453               | 291.64%            | 150         | 0.0133     | 8.1833              |
| 200         | 371           | 12     | 3.23%   | 1401               | 277.63%            | 200         | 0.0836     | 4.6167              |
| 500         | 371           | 9      | 2.43%   | 2159               | 481.94%            | 278         | 0.0164     | 10.6959             |
| 1000        | 371           | 18     | 4.85%   | 5392               | 1353.37%           | 301         | 0.0623     | 8.4191              |

$size = 4000$

| Window Size | Packets Sent | Errors | Error % | Total Transmitted | Retransmissions % | Max Window | RTT (sec) | Bandwidth (Mbit/s) |
|-------------|---------------|--------|---------|--------------------|--------------------|-------------|------------|---------------------|
| 10          | 130           | 1      | 0.77%   | 133                | 2.31%              | 10          | 0.0799     | 12.7528             |
| 50          | 130           | 8      | 6.15%   | 316                | 143.08%            | 50          | 0.0399     | 7.0935              |
| 100         | 130           | 19     | 14.62%  | 713                | 448.46%            | 79          | 0.0862     | 3.7426              |
| 500         | 130           | 17     | 13.08%  | 1160               | 792.31%            | 131         | 0.0923     | 5.0996              |
| 1000        | 130           | 26     | 20.00%  | 1521               | 1070.00%           | 131         | 0.0894     | 3.6840              |

### Localhost 
$size = 10000$
| Window Size | Packets Sent | Errors | Error % | Total Transmitted | Retransmissions % | Max Window | RTT (sec) | Bandwidth (Mbit/s) |
|-------------|---------------|--------|---------|--------------------|--------------------|-------------|------------|---------------------|
| 1           | 61657         | 0      | 0.00%   | 61657              | 0.00%              | 1           | 0.0006     | 69.1787             |
| 10          | 61657         | 0      | 0.00%   | 61657              | 0.00%              | 10          | 0.0776     | 109.8475            |
| 12          | 61657         | 3709   | 6.02%   | 106164             | 72.18%             | 12          | 0.0083     | 14.0797             |
| 15          | 61657         | 4630   | 7.51%   | 131102             | 112.63%            | 15          | 0.0163     | 13.3950             |
| 50          | 61657         | 4674   | 7.58%   | 295357             | 379.03%            | 50          | 0.0105     | 13.5379             |
| 100         | 61657         | 4693   | 7.61%   | 530180             | 759.89%            | 100         | 0.0143     | 13.8594             |
| 500         | 61657         | 4644   | 7.53%   | 2382101            | 3763.47%           | 500         | 0.0197     | 14.5650             |
| 1000        | 61657         | 7780   | 12.62%  | 7718828            | 12418.98%          | 1000        | 0.0600     | 20.1761             |


## Análisis

Para anakena se obtuvo un valor de RTT en torno a 50 ms tal como mencionó el profe en el foro (13 - 95 ms). Para una ventana de tamaño 1, se obtiene un ancho de banda muy bajo (comparable con los resultados de la tarea 3) y se tiene un "óptimo" para un tamaño de 10-15 y para valores mayores el ancho de banda no mejora. Cabe destacar que para localhost se utilizó el máximo de tamaño de ventana disponible y para anakena solo para tamaños menores a 200 (aproximadamente y solo considerando los casos inspeccionados). Además, se puede observar que para tamaños de ventana muy grande los errores obtenidos se disparan calzando con lo esperado teóricamente y vistos en el simulador visto en clases.

***Respuestas a preguntas de enunciado***:

1. Stop and Wait: No obtuve exactamente lo mismo que la tarea pasada (la implementación anterior no era muy buena) pero sí el ancho de banda es mucho menor que para los otros tamaños de ventana.
2. El protocolo funciona igual, no se cae. Como el que verifica el orden de los paquetes en este caso es la función Rdr y espera un número de secuencia en específico no falla. El caso esperado teóricamente para que falle se descarta pues simplemente no es el paquete esperado. Debería fallar si se cambia la forma de tratar los ack.
3. Esta propiedad se pierde. Pues si se envían los paquetes del 0 al 9, el recibidor en este caso es el otro proceso (función Rdr), y espera un número de secuencia en particular, si no recibe del 0 al 8, por ejemplo, y recibe el 9 este se descartará hasta que llegue el 0 primero.