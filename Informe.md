## Introduccion
En este proyecto simularemos un sistema de eventos discreto, mas especificamente un sistema donde un grupo de servidores, colocados en serie, atienden a clientes que tienen la necesidad de pasar por cada uno de los servidores en el orden en que aparecen. La llegada de los clientes asi como el tiempo de atencion en cada uno de los servidores estan dados por variables aleatorias de diferente distribucion, especificadas al comienzo de la Simulacion
### Objetivos y Metas
Queremos en primer lugar disenhar una estructura que permita simular el sistema, para cualquier combinacion de distribuciones. Una vez disenhada tal estructura, queremos estudiar las diferentes formas de colocar los servidores en la fila al saber de antemano la distriucion del tiempo de los servicios que brindan. De esta manera, podremos saber un poco mas sobre cual es la manera correcta de distribuir los servidores, para minimizar ya sea el tiempo que los clientes esperan en colas, la cantidad de colas que realizan o el tiempo de inactividad de cada servidor
### Descripcion del sistema
A continuacion la descripcion del sistema tal y como aparece en la orden:

Los clientes llegan a un sistema que tiene n servidores, y las llegadas distribuye M. Cada cliente que llega debe ser atendido primero por el servidor 1 y, al completar el servicio en el servidor 1, el cliente pasa al servidor 2.

Cuando un cliente llega, entra en servicio con el servidor 1 si ese servidor está libre, o se une a la cola del servidor 1 en caso contrario. De manera similar, cuando el cliente completa el servicio en el servidor 1, entra en servicio con el servidor 2 si ese servidor está libre, o se une a su cola y asi sucesivamente. Después de ser atendido en el servidor n, el cliente abandona el sistema.
### Variables de Interes
Estamos interesados en el tiempo de espera promedio por cliente, los tiempos maximo y promedio de inactividad de los servidores, la mayor longitud alcanzada por la cola de cualquier servidor, asi como la longitud promedio en la cola de cada servidor

## Como correrlo
Para usar una interfaz visual un pelin mas atractiva que la consola, usamos la libreria streamlit. Luego, para correr la simulacion, usted debera hacer:

streamlit run src/simulate.py

## Implementacion
Para la implementacion, creamos una clase Serial_Servers_Sim. Al instanciar esta clase le pasamos todas las distribuciones, digase la de la llegada de clientes y las relativas al tiempo de servicio de cada servidor. Esta clase tiene un atributo timeline, que no sera otra cosa sino la lista de eventos de la simulacion. Ademas esta clase tiene una tabla donde almacenara los datos generados por la simulacion. En tal tabla, a cada cliente corresponde una fila y a cada servidor una colummna, y las entradas de la tabla tienen la forma de tuplas donde aparecen el tiempo de llegada del cliente a la cola del servidor, el momento en que comenzo a ser atendido y el momento en que dejo el servidor.

Para realizar la simulacion, se requiere un parametro time (el tiempo a simular). Luego, usando la distribucion que haya sido provista para simular los intervalos de tiempo entre las llegadas de clientes, obtenemos una lista de numeros que siga tal distribucion y cuya suma no sobrepase time. Tal lista correspondera a los intervalos de tiempo de llegadas de clientes hasta el tiempo time, a partir del cual asumimos no llega ningun nuevo cliente.
Teniendo asi las llegadas que ocurriran, podemos construir la tabla, colocando una columna por cada cliente.
Los eventos en timeline son tuplas, que como primera componente tienen el momento de ocurrencia del evento, como segunda la naturaleza del evento "ARRIVAL", "BEGIN_SERVICE" o "FINISHED_SERVICE", como tercera el id del cliente y como cuarto el id del servidor. timeline es una cola de prioridad, que ordena los eventos por tiempo de ocurrencia en orden creciente.

La clase Serial_Servers_Sim, cuenta ademas con una lista de objetos de tipo Service. Cada objeto de tipo Service maneja la informacion relacionada con uno de los servidores en particular. Creimos necesario modelar a los servidores de esta manera, puesto que nos seria muy dificil extraer de la tabla del postprocesado informacion relativa al tamanho de la cola de cada servidor. Ademas un servidor debe manejar cierta logica para manejar su cola de clientes, y dado que el numero de servidores en cualquier simulacion con sentido va a ser muchisimo menor que el numero de clientes, el costo computacional de levantar una instancia por cada servidor no representara un cuello de botella. Por razones opuestas decidimos no modelar a los clientes como una clase, y extraer toda la informacion relativa a ellos en el post procesado de la tabla que generamos durante la simulacion. O sea, tales razones opuestas serian: el poco valor que tiene para cualquier estudio diferenciar la informacion de lo que ocurrio a un cliente en particular, pues la masa de los clientes es tratada como homogenea e infinita; la enorme cantidad de clientes que provocarian un costo computacional elevado al tener que instanciar una clase para cada uno de ellos; y ademas la ausencia de una logica a modelar para los clientes, ellos tan solo fluyen, como el agua. Por supuesto si se quisieran hacer simulaciones donde, por ejemplo, los clientes se asustaran en caso de encontrar una cola muy larga y se marcharan, comenzaria a tener sentido crear una abstraccion para ellos.

Cada instancia de tipo Service, cuenta con metodos para manejar cada uno de los eventos. Al ser llamados, le es pasado a la instancia el tiempo en que estamos en la ejecucon, de manera que puede actualizar sus datos, haciendo uso de una funcion interna suya update_time

La clase Serial_Servers_Sim ademas, tiene metodos para manejar cada uno de los eventos y un metodo para el post_procesado, que consiste meramente en iterar por cada fila y cada columna de la tabla para recuperar los datos de interes.

## Modelo Matematico
El modelaje matematico es el de un sistema de colas donde asumimos poblacion infinita. Asumimos llegada de clientes a intervalos de tiempo de distribucion exponencial. Si bien nuestro sistema tolera que se coloque cualquier otra distribucion para la llegada de clientes, verdaderamente no creemos que tenga entido usar otra. Los servidores tienen un tiempo de servicio que distribuye acorde a como el usuario de la simulacion establezca.

### Supuestos y Restricciones
Asumimos que automaticamente cuando un servidor termina de atender a un cliente, pasa al siguiente en la cola.
Asumimos que al cliente no le toma tiempo moverse de una cola a otra
Luego, esta simulacion es mas cercana a lo que ocurre en sistemas similares computarizados