# Tarea 5: Cliente eco UDP con Selective Repeat para medir performance
Los archivos utilizados en esta tarea son:
- `client_sr.py` donde se configura el cliente.
- `utils.py` donde se definen las clases packet y window utilizadas para implementar el protocolo gbn.
- `jsockets.py` archivo que se importa en el script del cliente.
- `archivo500KB.bin` archivo de entrada para el experimento. 
- `archivo600MB.bin` archivo de entrada para el experimento en localhost (no se incluye). 
- `logAnakena.bin` archivo que contiene los resultados de los experimentos con host anakena.
- `logLocal.bin` archivo que contiene los resultados de los experimentos con local host.

## Implementación 
En `client_sr.py` se encuentran definidas las funciones para comunicarse con un servidor vía sockets mediante el protocolo UDP implementando selective repeat. En el script `utils.py` se definen las clases Window, WindowRcv y Packet que se utiliza en la implementación del protocolo. La implementación del sender y el reader fue siguiendo el pseudo código del enunciado de la tarea.
## Mediciones
Para medir el ancho de banda (wb) se realizaron experimentos que usa `client_sr.py`. Los servidores utilizados fueron anakena.dcc.uchile.cl y localhost.

Con anakena se probó con dos size (1400 y 4000) y en localhost con size = 10000 inspeccionando tamaños de ventana de 1 hasta 1000 y con un timeout inicial de 0.1.
### Localhost
$size = 10000$
| Window Size | Packets Sent  | Packets Transmitted  | Error (%) | Estimated RTT (s) | Final Timeout (s) | Bandwidth (Mbit/s)  | Error (%) GBN | Bandwidth (Mbit/s) GBN|
|-------------|---------------|----------------------|-----------|-------------------|-------------------|---------------------|---------------|-------------------|
| 1           | 61657         | 62105                | 0.72      | 0.0010            | 0.0015            | 59.7689             |0.0|69.1787|
| 10          | 61657         | 62501                | 1.35      | 0.0078            | 0.0117            | 76.0233             |0.0|109.8475|
| 12          | 61657         | 62906                | 1.99      | 0.0211            | 0.0317            | 80.2692             |41.9|14.0797|
| 15          | 61657         | 69783                | 11.64     | 0.0141            | 0.0211            | 61.9701             |52.9|13.3950|
| 50          | 61657         | 149576               | 58.78     | 0.0093            | 0.0139            | 55.4550             |79.1|13.5379|
| 100         | 61657         | 251642               | 75.50     | 0.0407            | 0.0611            | 41.9475             |88.3|13.8594|
| 500         | 61657         | 8898237              | 99.31     | 0.0014            | 0.0021            | 24.8437             |97.4|14.5650|
| 900         | 61657         | 684245               | 90.99     | 0.0227            | 0.0341            | 55.6034             |99.2|20.1761|

### Anakena 
$size = 1400$
| Window Size | Packets Sent | Packets Transmitted | Error (%) | Estimated RTT (s) | Final Timeout (s) | Bandwidth (Mbit/s) | Error (%) GBN | Bandwidth (Mbit/s) GBN|
|-------------|---------------|----------------------|-----------|-------------------|-------------------|---------------------|---------------|-------------------|
| 1           | 371           | 373                  | 0.54      | 0.0105            | 0.0157            | 0.9498              |0.0|0.8283|
| 10          | 371           | 373                  | 0.54      | 0.0170            | 0.0254            | 7.6802              |3.4|5.0400|
| 15          | 371           | 383                  | 3.13      | 0.0093            | 0.0139            | 11.7878             |0.0|10.3402|
| 20          | 371           | 383                  | 3.13      | 0.0109            | 0.0163            | 13.2802             |7.7|9.7453|
| 50          | 371           | 400                  | 7.25      | 0.0118            | 0.0177            | 20.0262             |15.2|5.2377|
| 80          | 371           | 384                  | 3.39      | 0.0166            | 0.0248            | 26.5864             |5.3|9.5982|
| 100         | 371           | 383                  | 3.13      | 0.0387            | 0.0580            | 20.3755             |40.1|12.5920|
| 150         | 371           | 403                  | 7.94      | 0.0193            | 0.0289            | 23.4830             |74.4|8.1833|
| 200         | 371           | 1207                 | 69.26     | 0.0092            | 0.0139            | 13.8767             |73.5|4.6167|
| 500         | 371           | 1839                 | 79.83     | 0.0427            | 0.0641            | 6.2612              |82.8|10.6959|
| 999         | 371           | 1400                 | 73.50     | 0.0415            | 0.0623            | 7.7400              |93.1|8.4191|

### Anakena 
$size = 4000$
| Window Size | Packets Sent | Packets Transmitted | Error (%) | Estimated RTT (s) | Final Timeout (s) | Bandwidth (Mbit/s) | Error (%) GBN | Bandwidth (Mbit/s) GBN|
|-------------|---------------|----------------------|-----------|-------------------|-------------------|---------------------|---------------|-------------------|
| 10          | 130           | 131                  | 0.76      | 0.0120            | 0.0180            | 17.0749             |2.3|12.7528|
| 50          | 130           | 131                  | 0.76      | 0.0465            | 0.0698            | 26.9882             |58.9|7.0935|
| 100         | 130           | 157                  | 17.20     | 0.0248            | 0.0371            | 29.2802             |81.8|3.7426|
| 500         | 130           | 228                  | 42.98     | 0.0792            | 0.1188            | 9.9700              |88.8|5.0996|
| 999         | 130           | 318                  | 59.12     | 0.0778            | 0.1167            | 8.6515              |91.5|3.6840|

## Análisis

Para anakena se obtuvo un valor de RTT en torno a 10-50 ms tal como mencionó el profe en el foro (13 - 95 ms). Para una ventana de tamaño 1, se obtiene un ancho de banda muy bajo (comparable con los resultados de la tarea 3) y se tiene un "óptimo" para un tamaño de 12 en localhost y cercano a 80 en anakena, para valores mayores el ancho de banda no mejora. 
El timeout de retransmisión fue fijado en 0.1 inicialmente y `Final Timeout` es un parámetro que indica el valor del timeout de retransmisión al finalizar la comunicación, ya que se implementó un timeout variable. 
Además, se puede observar que para tamaños de ventana muy grande los errores obtenidos se disparan calzando con lo esperado teóricamente y vistos en el simulador visto en clases. Sin embargo, los errores obtenidos para selective repeat son menores en general a los errores obtenidos en go-back-n (últimas dos columnas de cada tabla) y con esto se obtuvo un mejor ancho de banda en esta tarea comparado con la anterior.

***Respuestas a preguntas de enunciado***:

1. Stop and Wait: Al observar la primera fila de las tablas se puede observar que se tienen valores muy similares y mucho menores que los resultados obtenidos para otros valores de tamaño de ventana. Con esto podemos decir que se rescata el comportamiento de stop and wait.
2. Teóricamente el tamaño máximo de ventana sería 500 y a pesar de que el protocolo sigue funcionando para valores mayores, el porcentaje de error crece considerablemente. En esta parte complicaciones pues al fijar el tamaño de ventana 1000, el algoritmo lanzaba un error probablemente por la numeración de la ventana de recepción por lo que tuve que realizar la simulación con un valores un poco menores.

