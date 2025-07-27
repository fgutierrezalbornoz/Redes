# Tarea 6: Cliente eco UDP con Selective Repeat Adaptativo para medir performance
Los archivos utilizados en esta tarea son:
- `client_sr2_bw.py` donde se configura el cliente.
- `utils.py` donde se definen las clases packet y window utilizadas para implementar el protocolo gbn.
- `jsockets.py` archivo que se importa en el script del cliente.
- `archivo500KB.bin` archivo de entrada para el experimento. 
- `archivo600MB.bin` archivo de entrada para el experimento en localhost (no se incluye). 
- `logAnakena.bin` archivo que contiene los resultados de los experimentos con host anakena.
- `logLocal.bin` archivo que contiene los resultados de los experimentos con local host.

## Implementación 
En `client_sr2_bw.py` se encuentran definidas las funciones para comunicarse con un servidor vía sockets mediante el protocolo UDP implementando selective repeat, esta vez con timeout y rtt adaptativo. En el script `utils.py` se definen las clases Window, WindowRcv y Packet que se utiliza en la implementación del protocolo. La implementación está basada en la tarea 5 y se agregan los cambios para incluir timeouts y rtt adaptativos además de la ventana de congestión.

Respecto a la tarea pasada en `utils.py` solo cambié la forma de calcular el RTT. Antes se calculaba con un promedio y ahora como el máximo tal como se indica en el enunciado.
## Mediciones
Para medir el ancho de banda (wb) se realizaron experimentos que usa `client_sr2_bw.py`. Los servidores utilizados fueron anakena.dcc.uchile.cl y localhost.

Con anakena se probó con size = 4000 y en localhost con size = 10000 inspeccionando tamaños de ventana de 1 hasta 1000 y con un timeout inicial de 1.

### Anakena 
$size=1400$
| Window Size | Packets Sent  | Packets Transmitted  | Error (%)  | Estimated RTT (s)  | Final Timeout (s)  | Bandwidth (Mbit/s)   | Cong Win Size  | Error (%) (T5) | Bandwidth (Mbit/s) (T5) |
|-------------|---------------|----------------------|------------|--------------------|--------------------|----------------------|----------------|----------------|-------------------------|
| 1           | 371           | 371                  | 0.00       | 0.0093             | 0.0187             | 1.5629               | 1              | 0.54  | 0.9498  |
| 10          | 371           | 371                  | 0.00       | 0.0386             | 0.0772             | 9.9908               | 10             | 0.54  | 7.6802  |
| 15          | 371           | 371                  | 0.00       | 0.0182             | 0.0364             | 15.4409              | 15             | 3.13  | 11.7878 |
| 20          | 371           | 371                  | 0.00       | 0.0125             | 0.0251             | 17.4582              | 20             | 3.13  | 13.2802 |
| 50          | 371           | 371                  | 0.00       | 0.0193             | 0.0386             | 26.2452              | 50             | 7.25  | 20.0262 |
| 80          | 371           | 371                  | 0.00       | 0.0280             | 0.0560             | 25.7634              | 80             | 3.39  | 26.5864 |
| 100         | 371           | 378                  | 1.85       | 0.0503             | 0.1005             | 17.2500              | 25             | 3.13  | 20.3755 |
| 150         | 371           | 379                  | 2.11       | 0.0281             | 0.0562             | 25.3464              | 75             | 7.94  | 23.4830 |
| 200         | 371           | 373                  | 0.54       | 0.0537             | 0.1073             | 14.4035              | 100            | 69.26 | 13.8767 |
| 400         | 371           | 735                  | 49.52      | 0.1862             | 2.0000             | 0.6426               | 50             | -     | - |
| 500         | 371           | 616                  | 39.77      | 0.0422             | 2.0000             | 0.9719               | 64             | 79.83 | 6.2612  |
| 999         | 371           | 725                  | 48.83      | 0.0722             | 2.0000             | 0.7343               | 125            | 73.50 | 7.7400  |

### Localhost 
$size=10000$

| Window Size | Packets Sent  | Packets Transmitted  | Error (%)  | Estimated RTT (s)  | Final Timeout (s)  | Bandwidth (Mbit/s)  | Cong Win Size   | Error (%) (T5) | Bandwidth (Mbit/s) (T5) |
|-------------|---------------|----------------------|------------|--------------------|--------------------|----------------------|----------------|----------------|-------------------------|
| 1           | 61657         | 61657                | 0.00       | 0.0065             | 0.0130             | 56.4962              | 1              | 0.72  | 59.7689 |
| 10          | 61657         | 61657                | 0.00       | 0.0288             | 0.0576             | 97.8808              | 10             | 1.35  | 76.0233 |
| 12          | 61657         | 61658                | 0.00       | 0.0107             | 0.0214             | 102.5996             | 6              | 1.99  | 80.2692 |
| 15          | 61657         | 61659                | 0.00       | 0.0175             | 0.0349             | 106.1491             | 8              | 11.64 | 61.9701 |
| 50          | 61657         | 61700                | 0.07       | 0.0119             | 0.0239             | 95.5081              | 7              | 58.78 | 55.4550 |
| 100         | 61657         | 61914                | 0.42       | 0.0155             | 0.0619             | 90.3573              | 2              | 75.50 | 41.9475 |
| 400         | 61657         | 63882                | 3.48       | 0.0251             | 0.0501             | 59.9864              | 2              | - | -|
| 500         | 61657         | 65457                | 5.81       | 0.0227             | 0.0453             | 53.9486              | 2              | 99.31 | 24.8437 |
| 900         | 61657         | 69437                | 11.20      | 0.0221             | 0.0442             | 45.0333              | 2              | 90.99 | 55.6034 |


## Análisis
Se realizó una medición con tamaño de ventana igual a 400 ya que era el ejemplo del enunciado pero no hay una medición de la T5 con el cual comparar. Las últimas dos columnas son los resultados de la tarea 5.

Un resultado curioso y que no sabría explicar el porqué es el tamaño de la ventana de congestión para localhost (que tiene un mínimo de 2 para hartos tamaños de ventana). Probé disminuyendo el tamaño del paquete incluso hasta 1400 bytes pero no aumentaba mucho (tamaño mínimo ~ 60).

***Respuestas a preguntas de enunciado***:
1. Comparación con T5: 
Se puede observar que se obtiene una cantidad significativamente menor en cuanto error debido a la implementación de la ventana de congestión. Respecto al timeout no se obtiene gran diferencia con respecto a la T5 ya que había implementado el RTT variable, sin embargo, se observa que estos disminuyen a un valor cercano a los valores mencionados por el profesor en el foro.

    En cuanto al bw se observa que se tienen mejores métricas con respecto a la T5 con lo que se concluye que efectivamente resulta ser más eficiente que el método anterior.
2. Escenario en el que tiene peor desempeño que T5: Sí, podemos observar que para tamaños muy grande de ventana se obtienen peores resultados para el ancho de banda.
