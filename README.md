# Practica-2
Puente de Ambite

El archivo practica2.py es una solución para un problema en el que hay un túnel de un solo sentido que puede ser cruzado por coches y peatones. Sin embargo, esta versión no considera la cantidad de coches que pasan juntos, lo que puede hacer que los peatones tengan que esperar mucho tiempo para cruzar. Aunque esta solución asegura la seguridad.
NCARS: Número total de coches que se espera que pasen por el túnel.
NPED: Número total de peatones que se espera que pasen por el túnel.
TIME_CARS: Tiempo de espera entre la aparición de dos coches seguidos.
TIME_PED: Tiempo de espera entre la aparición de dos peatones seguidos.
TIME_IN_BRIDGE_CARS: Tiempo que tarda un coche en atravesar el túnel (en segundos).
TIME_IN_BRIDGE_PEDESTRGIAN: Tiempo que tarda un peatón en atravesar el túnel (en segundos).

El archivo practica2_1.py es una solución para un problema en el que hay un túnel de un solo sentido que puede ser cruzado por coches y peatones. Esta versión considera la cantidad de coches o peatones que pasan juntos, lo que puede hacer que los peatones p coches tengan que esperar menos tiempo para cruzar. Esta solución asegura la seguridad.
En esta version se implementan algunas constantes más:

Seguidos_coches: número máximo de coches seguidos que pueden pasar en una misma dirección antes de que se permita el paso de los peatones.
Seguidos_peatones: número máximo de peatones seguidos que pueden pasar antes de que se permita el paso de los coches en la otra dirección.

En ambos al ejecutar el programa, se mostrarán en la consola los registros de los eventos que ocurren. En particular, se muestra la cantidad de coches y peatones que pasan por el túnel, y se notifica cada vez que se produce un cambio en la situación, como el paso de un coche o peatón.

Los códigos utilizan la biblioteca multiprocessing para permitir la ejecución de procesos concurrentes. El monitor es utilizado para coordinar la entrada y salida de coches y peatones en el túnel. El monitor utiliza un objeto de bloqueo y una condición para evitar que los procesos se ejecuten simultáneamente.

El código tiene tres funciones delay_ que son utilizadas para simular el tiempo que un coche o un peatón tarda en cruzar el túnel. También tiene las funciones car y pedestrian que son ejecutadas por los procesos de coches y peatones, respectivamente. Estas funciones utilizan el monitor para coordinar la entrada y salida del túnel y para asegurar que sólo un coche o peatón cruza el túnel a la vez.

Los archivos txt nos muestran los resultados al ejecutar los archivos.
El archivo pdf nos da una especificacion del codigo y nos indica en que casos se nos asegura la concurrencia, la seguridad, vivacidad y la justicia
