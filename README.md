# Proyecto-I-de-Simulacion

### Orientacion
Los clientes llegan a un sistema que tiene n servidores, y las llegadas distribuye M. Cada cliente que llega debe ser atendido primero por el servidor 1 y, al completar el servicio en el servidor 1, el cliente pasa al servidor 2.

Cuando un cliente llega, entra en servicio con el servidor 1 si ese servidor está libre, o se une a la cola del servidor 1 en caso contrario. De manera similar, cuando el cliente completa el servicio en el servidor 1, entra en servicio con el servidor 2 si ese servidor está libre, o se une a su cola y asi sucesivamente. Después de ser atendido en el servidor n, el cliente abandona el sistema.

Los tiempos de servicio en el servidor i tienen la distribución Gi

### Componentes de la estructura de un sistema de colas
-Poblacion
-Llegadas
-Colas
-Sistemas de Seleccion
-Unidad de Servicios
-Salidas

### Detalles de implementacion
Podemos asumir poblacion infinita, o sea, no modelarla

