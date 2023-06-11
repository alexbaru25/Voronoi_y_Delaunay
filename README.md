       
# Voronoi_y_Delaunay

Este trabajo se basa en el repositorio de GitHub de Janson Hendryli, disponible en [https://github.com/jansonh/Voronoi.git](https://github.com/jansonh/Voronoi.git). Se han agregado comentarios a todas las funciones para facilitar la comprensión del código. Además, se ha implementado la opción de computar la triangulación de Delaunay.

El objetivo de este programa es computar diagramas de Voronoi y triangulaciones de Delaunay utilizando el algoritmo de Fortune. El programa está escrito en Python y utiliza la biblioteca tkinter para graficar los resultados obtenidos.

## Instrucciones de ejecución

1. Ejecuta el archivo `main.py`.
2. En la ventana emergente, añade nodos haciendo doble clic en la pantalla.
3. Para computar el diagrama de Voronoi, haz clic en el botón "Voronoi". Para eliminar los nodos de la pantalla, haz clic en el botón "Clear". Para computar la triangulación de Delaunay, haz clic en el botón "Delaunay".
4. Para cerrar la ventana, haz clic en la cruz ubicada en la parte superior derecha de la ventana.

## Descripción del código

El código está organizado en varios archivos para facilitar su comprensión:

### main.py

Este archivo se encarga de generar los botones y opciones de la interfaz de usuario.

### DataType.py

Este archivo contiene la definición de varias clases utilizadas en el programa:

- La clase `Point` representa un punto en el plano.
- La clase `Event` representa un evento y tiene componentes como `x` (radio de la circunferencia), `p` (centro de la circunferencia) y `a` (arco relacionado al evento).
- La clase `Arc` representa un arco de la línea de playa y tiene componentes como `p` (nodo que genera el arco), `pprev` (arco anterior), `pnext` (arco siguiente), `e` (evento relacionado al arco), `s0` (segmento generado entre el arco y `pprev`) y `s1` (segmento generado entre el arco y `pnext`).
- La clase `Segment` representa un segmento del diagrama de Voronoi y tiene componentes como `start` (punto de inicio del segmento), `end` (punto final del segmento) y `done` (indica si el segmento ha sido completado).
- La clase `PriorityQueue` representa una cola de prioridad y tiene métodos como `push` (para insertar elementos), `top` (para obtener el elemento con mayor prioridad), `pop` (para obtener y eliminar el elemento con mayor prioridad) y `empty` (para verificar si la cola de prioridad está vacía).

### Voronoi.py

Este archivo contiene la implementación principal del algoritmo de línea de barrido para computar los diagramas de Voronoi y triangulaciones de Delaunay.

- La clase `Voronoi` representa el programa en sí. Toma como entrada los nodos y si se desea computar la triangulación de Delaunay.
  - En el método `__init__`, se realizan las inicializaciones necesarias, como la creación de listas para almacenar los segmentos de los diagramas de Voronoi y triangulaciones de Delaunay, la inicialización de un árbol binario, colas de prioridad para puntos y circunferencias de eventos, una caja para unir los segmentos incompletos, y la inserción de los puntos iniciales en la cola de prioridad de puntos.
  - La clase `Voronoi` también implementa varias funciones internas para computar el problema:
    - `process` es la función principal que maneja el movimiento de la línea de barrido a través de los eventos. Procesa las circunferencias y puntos de eventos en el orden correcto y luego une los segmentos incompletos al final.
    - `process_point` se encarga de procesar los puntos de eventos. Obtiene el punto de eventos con mayor prioridad de la cola de prioridad, lo elimina de la cola y lo inserta en el árbol.
    - `process_event` maneja las circunferencias de eventos. Extrae el evento de circunferencia con mayor prioridad de la cola, verifica su validez y realiza las operaciones necesarias para crear un nuevo segmento, eliminar el arco asociado al evento y finalizar los segmentos relacionados a ese arco. Luego, verifica si las circunferencias de eventos circundantes han sido modificadas y actualiza los eventos relacionados si es necesario.
    - `arc_insert` se encarga de insertar un nuevo arco en el árbol de parábolas. Si el árbol está vacío, se crea un nuevo árbol con el arco correspondiente al nodo dado. Si el árbol no está vacío, se recorre para encontrar la posición adecuada para insertar el nuevo arco, realizando intersecciones y actualizaciones si es necesario.
    - `check_circle_event` verifica si hay una nueva circunferencia de eventos asociada a un arco en el árbol de parábolas. Si existe una circunferencia de eventos previamente asignada y es válida, se crea un nuevo evento de circunferencia y se agrega a la cola de prioridad de eventos.
    - `circle` determina si tres puntos forman una circunferencia válida utilizando cálculos basados en el producto vectorial de Gibbs y las ecuaciones de las mediatrices.
    - `intersect` verifica si un arco intersecta con otro arco representado por un punto dado. Si hay una intersección, se calcula el punto exacto de intersección.
    - `intersection` calcula la intersección entre dos parábolas definidas por nodos y una directriz utilizando la ecuación general de una parábola.
    - `finish_edges` se utiliza para completar los segmentos que aún no han sido finalizados al finalizar el proceso de línea de barrido.
    - `get_output` devuelve una representación visual del diagrama de Voronoi en forma de lista, que contiene las coordenadas de los puntos de inicio y fin de cada segmento.
    - `get_del` devuelve una representación visual de la triangulación de Delaunay en forma de lista, que contiene las coordenadas de los puntos de inicio y fin de cada segmento.

            



































   
