# Tarea 2: Cliente eco UDP para medir performance

Los archivos utilizados en esta tarea son:
- `client_echo_udp3.py` donde se configura el cliente.
- `jsockets.py` archivo que se importa en el script del cliente.
- `archivo500KB.bin` archivo de entrada para el experimento 1. 
- `archivo10KB.bin` archivo de entrada para el experimento 2.
- `logAnakena.bin` archivo que contiene los resultados de los experimentos.
## Mediciones
Para medir el ancho de banda (wb) se realizaron 2 experimentos. Ambos están programados en el script `Tarea2.py` que usa `client_echo_udp3.py`. En este último se encuentran definidas las funciones para comunicarse con un servidor vía sockets mediante el protocolo UDP. En ambos experimentos se usó anakena como servidor.
### Experimento 1
Se pobró con distintos tamaños de lectura/escritura para un archivo de 500KB (`archivo500KB.bin`). Los resultados fueron:

|Size [B]|Ancho de Banda [MB/s]|Porcentaje de pérdida|
|-|-|-|
|1000|190.8|0|
|1000|229.5|15.2|
|2000|355.8|62.9|
|3000|523.6|34.7|
|4000|828.2|27.8|
|5000|474.8|0|
|6000|915.7|0|
|7000|328.2|5.4|
|8000|997.5|18.5|
|9000|528|1.7|
|10000|669|3.8|

### Experimento 2
El experimento consistió en enviar una cantidad de veces un archivo usando threads, en donde cada threads enviaba un archivo y luego recibía la respuesta del servidor.
Se consideró la misma cantidad de threads utilizados en la tarea 1, 80 threads en total.

|Size [B]|Ancho de Banda [KB/s]|Porcentaje de pérdida|
|-|-|-|
|1000|66.3|0|
|1000|67.3|0|
|2000|65.3|0|
|3000|61.2|0|
|4000|257.3|0.2|
|5000|254|6|
|6000|252.7|4.2|
|7000|248.8|3.8|
|8000|196.4|0.2|
|9000|257.5|2.3|
|10000|225.9|10.5|

## LocalHost
Intenté realizar los experimentos en localhost utilizando un archivo de ~600MB pero siempre obtuve midiciones inválidas en las cuales se tenía una pérdida > 80%. Probé con los mismos size de los experimentos 1 y 2, incluso con size muy grandes (100000-500000) y muy pequeños (100) sin resultados exitosos (más detalles en `logLocal.bin`).

## Conclusión

Considerando los resultados obtenidos se observa que el ancho de banda en el primer experimento (O(MB)) es mucho mayor que la segunda (O(KB)) y puede tener su explicación en la cantidad de consultas a manejar lo que genera un delay en estas, además de un manejo de las consultas de forma poco eficiente.

Se observa que con el archivo grande (experimento 1) se tiene una mayor cantidad de pérdida de paquetes, puede estar relacionado con la cantidad de consultas que se debe responder en comparación con archivos pequeños.

Los resultados obtenidos en esta tarea son similares a grandes rasgos comparados con la tarea 1 (mencionado al inicio de la conclusión). Sin embargo se tienen problemas inherentes al uso de sockets UDP, con esto me refiero a que hubo muchas mediciones que resultaron siendo inválidas pues finalizaron debido a un timeout (más detalles en `logAnakena.bin`).

***Respuestas a preguntas de enunciado***:

1 y 2.-  Si se considera solo lo enviado/recibido se estaría midiendo un ancho de banda que se pretende utilizar pero no el efectivo. Además, se estaría asumiendo que se comporta de forma simétrica.
3.- Se podría utilizar siempre y cuando el tamaño de cada paquete de información sea pequeño, ya que de no ser así esto podría representar una pérdida de información significativa lo que genera una medición poco confiable.

*Obs*: En la ejecución de el segundo experimento se tiene un problema al guardar la información enviada por el servidor al cliente, esto puede deberse a un mal funcionamiento de los threads que se bloquean durante la ejecución. Esto puede darse debido a la implementación ya que la separación de los threads se hace en 4 grupos y en cada grupo un thread se encarga de separar el trabajo en más threads. 
