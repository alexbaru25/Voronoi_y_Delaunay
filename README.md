# Voronoi_y_Delaunay
Este es un trabajo basado en  https://github.com/jansonh/Voronoi.git de Janson Hendryli. Se han comentado todas las funciones para un mayor comprendimiento del trabajo. Además se ha implementando la opción de computar la triangulación de Delaunay. 

Consiste en computar con el algoritmo de Fortune diagramas de Voronoi y la triangulaciones de Delaunay, teniendo unos nodos como datos iniciales.
Este programa está implementado con Python y utiliza la libreria tkinter para graficar los resultados obtenidos.

Instrucciones de ejecucion:
  1. Ejecuta el archivo main.py
  2. En la ventana emergente, añadir nodos haciendo doble click en la pantalla emergente.
  3. Para computar el diagrama de Voronoi clicar en Voronoi, para eliminar los nodos de la ventana emergente clicar en Clear, y para computar la triangulación de Delaunay clicar en Delaunay
  4. Para cerrar la ventana pulsar la cruz que se encuentra en la parte superior derecha de la ventana

Descripcion del código

En main.py:
   Se generan los botones y las opciones de la interfaz

En DataType.py:
   -Se crea la clase Point, que representa un punto en el plano
   -Se crea la clase Event, representa un evento, en sus componentes:
        - 'x' representa el radio de la circunferencia   
        - 'p' representa el centro de la circunferencia
        - 'a' representa el arco que corresponde el evento
   -Se crea la clase Arc, representa un arco de la línea de playa, sus componentes son:
        -'p' representa el nodo que genera el arco
        -'pprev' representa  el arco previo,
        -'pnext' representa el arco siguiente
        -'e' representa el evento que tiene relación con el arco, sus componentes son:
        -'s0' representa al segmento que se genera entre el arco y 'pprev'
        -'s1' representa al segmento que se genera entre el arco y 'pnext'
   -Se crea la clase Segment, representa un segmento del diagrama de Voronoi, sus componentes son:
        -'start' representa el comienzo del segmento
        -'end' representa el final del segmento
        -'done' representa si ha finalizado el segmento
   - Se crea la clase PriorityQueue, representa una cola de prioridad, sus componentes son:
        - 'push' para introducir elementos en la cola de prioridad
        - 'top'  para obtener el elemento con mayor prioridad de la cola de prioridad
        - 'pop'  para obtener el elemento con mayor prioridad y eliminarlo de la cola de prioridad
        - 'empty' para conocer si la cola de prioridad está vacía
   
En Voronoi.py:
   -Se crea una clase Voronoi cuyos datos de entrada son los nodos y si se desea computar la triangulación de Delaunay.
       -En el init se realiza lo siguiente:
           -Se crea una lista para almacenar los segmentos que conforman los diagramas de Voronoi.
           -Se crea otra lista para almacenar los segmentos que conforman las triangulaciones de Delaunay.
           -Se inicializa un árbol binario.
           -Se inicializa una cola de prioridad para los puntos de eventos.
           -Se inicializa una cola de prioridad para las circunferencias de eventos.
           -Se crea una caja para unir todos los segmentos que no hayan finalizado su procesamiento.
           -Dado que se conocen previamente los puntos de eventos, introducimos en la cola llamada `self.points` los puntos que hemos indicado.
           -Si hay nodos que se encuentran fuera de la caja, es posible que sea necesario modificar las dimensiones de la caja 
            para asegurarnos de que todos los nodos se encuentren dentro de ella. 
           -Esto se hace para garantizar que los cálculos y las intersecciones de segmentos se realicen correctamente.
       - Se implementan divesas funciones internas para poder computar el problema:
            -La función `process` es la funcion principal del programa que maneja el movimiento de la línea de barrido a través de eventos.
             Procesa circunferencias y puntos de eventos en el orden correcto. Luego de procesar todos los eventos, se unen los
             segmentos incompletos para asegurar su conexión adecuada.
            - La función 'process_point' procesa los puntos de eventos. Obtiene el punto de eventos con mayor prioridad de la cola de prioridad, lo elimina de la cola, y lo inserta en el árbol.
            - La función 'process_event' maneja las circunferencias de eventos. Se extrae el evento de mayor prioridad de la cola de prioridad. Luego, se verifica si el evento es válido. Si es válido, se crea un nuevo                 segmento que comienza en el punto asignado al evento. Se realizan las operaciones necesarias para eliminar el arco asociado al evento y se finalizan los segmentos relacionados con ese arco. Después de esto,               se comprueba si las circunferencias de eventos circundantes han sido modificadas, y si es así, se actualizan los eventos relacionados y se vuelven a introducir en la cola de prioridad de eventos
              correspondiente.
            - La función `arc_insert` se encarga de insertar un nuevo arco en el árbol de parábolas. Si el árbol está vacío, se crea un nuevo árbol con el arco correspondiente al nodo 'p'. En caso contrario, se recorre                 el árbol para determinar si la parábola generada por el punto 'p' intersecta con algún arco existente en el árbol.
              Si se encuentra una intersección, se crean nuevos arcos y segmentos, y se actualizan los arcos existentes para insertar el nuevo arco entre ellos. Se verifican también las circunferencias de eventos para                 detectar posibles modificaciones. Si no se encuentra ninguna intersección, se agrega el nuevo arco al final del árbol.
            - La función 'check_circle_event' se encarga de verificar si hay una nueva circunferencia de eventos asociada al arco 'i' en el árbol de parábolas. Si existe una circunferencia de eventos anteriormente  asignada a 'i' y su coordenada x no es igual a 'x0', se marca como inválida para evitar su procesamiento. Luego, se verifica si el arco 'i' tiene un arco anterior y un arco siguiente. Si no los tiene, la función                   termina. En caso contrario, se comprueba si hay una circunferencia de eventos que satisfaga ciertas condiciones. Si se cumple, se crea un nuevo evento de circunferencia y se agrega a la cola de prioridad de               eventos.
            - La función 'circle' se encarga de determinar si los tres puntos dados (a, b, c) forman una circunferencia válida. Para ello, realiza una serie de cálculos basados en el producto vectorial de Gibbs y las  ecuaciones de las mediatrices.


            



































   
