# Tarea 1: Cliente eco TCP para medir performance

Los archivos utilizados en esta tarea son:
- `client_tarea.py` donde se configura el cliente.
- `jsockets.py` archivo que se importa en el script del cliente.
- `archivo500KB.txt` archivo de entrada para el experimento 1. 
- `archivo5KB.txt` archivo de entrada para el experimento 2.  
## Mediciones
Para medir el ancho de banda (wb) se realizaron 2 experimentos. Ambos están programados en el script `Tarea1.py` que usa `client_tarea.py`. En este último se encuentran definidas las funciones para conectarse a un servidor vía sockets mediante el protocolo TCP. En ambos experimentos se usó anakena como servidor.
### Experimento 1
Se pobró con distintos tamaños de lectura/escritura para un archivo de 500KB (`archivo500KB.txt`). Los resultados fueron:

|Size [B]|Ancho de Banda [MB/s]|
|-|-|
|1000|471.6|
|2000|599.9|
|3000|679.6|
|4000|355.4|
|5000|577.9|

### Experimento 2
El experimentó consistió en enviar una cantidad de veces un archivo usando threads, en donde cada threads enviaba un archivo y luego recibía la respuesta del servidor.
La primera parte del experimento consistió en medir el ancho de banda para distintas cantidades de threads, estas mediciones variaron mucho pero se encontraban entre los 10 KB/s y los 120 KB/s. Seguramente había error de ejecución pues la cantidad de bytes enviados/ recibidos no coinciden con los esperados ( probablemente errores de ejecución en paralelo)

|Size [B]|Ancho de Banda [KB/s]|
|-|-|
|1000|33.5|
|2000|48.1|
|3000|33.9|
|4000|47.3|
|5000|41.6|


## Conclusión

Considerando los resultados obtenidos se observa que el ancho de banda en el primer experimento (O(MB)) es mucho mayor que la segunda (O(KB)) y puede tener su explicación en la cantidad de consultas a manejar lo que genera un delay en estas, además de un manejo de las consultas de forma poco eficiente.
En la ejecución de los experimentos se tienen resultados variados y se consideró un promedio de estos.
En la ejecución de el segundo experimento se tiene un problema al guardar la información enviada por el servidor al cliente, esto puede deberse a un mal funcionamiento de los threads que se bloquean durante la ejecución. Esto puede darse debido a la implementación ya que la separación de los threads se hace en 4 grupos y en cada grupo un thread se encarga de separar el trabajo en más threads. El primer grupo es capaz de guardar bien los archivos pero los otros no. 
Con respecto a esto, no le puse mucha antención ya que la medición de la data recibida se captura antes de guardar el archivo.