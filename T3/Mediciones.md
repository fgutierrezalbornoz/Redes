# Tarea 3: Cliente eco UDP con Stop-and-Wait para medir performance

Los archivos utilizados en esta tarea son:
- `client_t3.py` donde se configura el cliente.
- `jsockets.py` archivo que se importa en el script del cliente.
- `archivo500KB.bin` archivo de entrada para el experimento. 
- `log_anakena.bin` archivo que contiene los resultados de los experimentos.
## Mediciones
Para medir el ancho de banda (wb) se realizó un experimento cuyo código está en el script `Tarea3.py` que usa `client_t3.py`. En este último se encuentran definidas las funciones para comunicarse con un servidor vía sockets mediante el protocolo UDP implementando stop and wait. El servidor utilizado fue anakena.dcc.uchile.cl.
### Experimento
Se pobró con distintos tamaños de lectura/escritura para un archivo de 500KB (`archivo500KB.bin`) y para distintos timeout de retransmisión. En primera instancia se midió el ping del servidor en el cual se obtuvo ~10ms, es por esto que el mínimo valor utilizado fue 0.03 segundos pues para valores menores el programa se quedaba en un loop retransmitiendo mensajes. Los resultados fueron:

Para timeout = 0.1
Notación p.p = paquetes perdidos
|Size [B]|Ancho de Banda [KB/s]|N° de paquetes enviados|N° de p.p|N° de p.p (EOF)|Porcentaje de p.p (%)|
|-|-|-|-|-|-|
|1000|36.8|625|107|107|17.1|
|2000|301.1|260|1|1|0.3|
|3000|381.4|174|1|1|0.5|
|4000|461.4|131|1|1|0.7|
|5000|488.2|106|2|1|0.9|
|6000|578.1|88|1|1|1.1|
|7000|591.8|75|1|1|1.3|
|8000|697.4|66|1|1|1.5|
|9000|623.9|60|2|1|3.3|
|10000|749.9|53|1|1|1.8|

Para timeout = 0.05
|Size [B]|Ancho de Banda [KB/s]|N° de paquetes enviados|N° de p.p|N° de p.p (EOF)|Porcentaje de p.p (%)|
|-|-|-|-|-|-|
|1000|30.7|770|252|248|32.7|
|2000|292.2|263|4|1|1.5|
|3000|395.1|174|1|1|0.5|
|4000|481.4|132|2|1|1.5|
|5000|574.2|105|1|1|0.9|
|6000|604.9|89|2|1|2.2|
|7000|678.4|75|1|1|1.3|
|8000|708.9|66|1|1|1.5|
|9000|720.9|59|1|1|1.6|
|10000|813.8|53|1|1|1.8|

Para timeout = 0.04
|Size [B]|Ancho de Banda [KB/s]|N° de paquetes enviados|N° de p.p|N° de p.p (EOF)|Porcentaje de p.p (%)|
|-|-|-|-|-|-|
|1000|41.5|745|227|224|30.4|
|2000|309.0|260|1|1|0.3|
|3000|409.3|175|2|1|1.1|
|4000|523.0|132|2|1|1.5|
|5000|584.5|105|1|1|0.9|
|6000|615.0|88|1|1|1.1|
|7000|703.6|75|1|1|1.3|
|8000|698.9|67|2|1|2.9|
|9000|767.5|61|3|1|4.9|
|10000|836.4|53|1|1|1.8|

Un timeout menor solo fue logrado con un size mayor 
timeout = 0.03
|Size [B]|Ancho de Banda [KB/s]|N° de paquetes enviados|N° de p.p|N° de p.p (EOF)|Porcentaje de p.p (%)|
|-|-|-|-|-|-|
|10000|865.7|54|2|1|3.7|
|15000|973.1|38|3|1|7.8|
|20000|1133.8|28|2|1|7.1|


## LocalHost
Intenté realizar los experimentos en localhost utilizando un archivo de ~600MB para probar timeouts menor sin éxito y los  valores utilizados en los resultados mostrados generaban experimentos que tomaban mucho tiempo.

## Conclusión

Considerando los resultados obtenidos se observa que el ancho de banda es O(KB) mucho menor de los valores obtenidos en la tarea 2 que eran O(MB), esto probablemente se debe a que la mayor parte del tiempo se toma para esperar la confirmación del recibimiento del mensaje. Para valores de `size` más bajo se tiene un muy bajo valor de banda ancha donde se espera casi la totalidad de timeout antes de enviar el siguiente mensaje. 
Se tiene un problema para detectar el EOF y estuve buscando que UDP a veces no reconoce paquetes muy pequeños y probablemente por esto se tiene malos rendimientos para `size` pequeño.
A pesar de la notoria baja en el valor obtenido para el ancho de banda, se mejora notablemente la pérdida de paquetes.



***Respuestas a preguntas de enunciado***:

1.- Podría haber problemas al momento de informar el recibimiento del paquete. Por ejemplo, se envía un paquete p1 que no llega en la ventana de tiempo que se define con el timeout, entonces se retransmite ese paquete p1 ahora en un paquete p1' y por alguna razón p1 llega luego de que se envía el paquete p3 entonces se enviaría el p4, si el paquete p3 se pierde el que recibe el mensaje no sabría que se perdió ese paquete ya que solo se verifica que no lleguen paquetes con el mismo número de secuencia de uno que ya llegó.

2.- Los valores de ancho de banda medidos en esta tarea sí son muy distintos a los de la T1 y T2. Yo creo que se debe principalmente que es debido al tiempo de espera entre el envío del mensaje y la confirmación de llegada de este, mientras mayor es el timeout menor es el ancho de banda obtenido. 
En las tareas anteriores se enviaba un mensaje tras otro y por lo tanto el tiempo total que tomaba al enviar la totalidad del archivo era menor.

3.- Si el protocolo se implementa bien, el socket permanece ocupado. Al fijar el timeout del socket para un tiempo máximo de espera, este contador se reinicia al retransmitir el mensaje siempre y cuando el timeout de retransmisión sea menor al de cierre del socket. Entonces, existen 2 escenarios el mensaje llega dentro del tiempo asignado o se retransmite, en ningún caso se llega al tiempo de timeout para cerrar el socket.

