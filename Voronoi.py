# -*- coding: utf-8 -*-
"""
Created on Wed May 17 14:09:15 2023

@author: Alex b
"""
import random
import math

from DataType import Point, Event, Arc, Segment, PriorityQueue


class Voronoi:
    def __init__(self, points,delau):
        """
        Se crea una lista para almacenar los segmentos que conforman los diagramas de Voronoi.
        Se crea otra lista para almacenar los segmentos que conforman las triangulaciones de Delaunay.
        Se inicializa un árbol binario.
        Se inicializa una cola de prioridad para los puntos de eventos.
        Se inicializa una cola de prioridad para las circunferencias de eventos.
        """
        self.delau=delau
        if self.delau:
           self.delaunay =[] #para Delaunay
        self.output = [] # list of line segment
        self.arc = None  # binary tree for parabola arcs

        self.points = PriorityQueue() # site events
        self.event = PriorityQueue() # circle events
        
        """
        Se crea una caja para unir todos los segmentos que no hayan finalizado su procesamiento.
        """

        # bounding box
        self.x0 = -50.0
        self.x1 = -50.0
        self.y0 = 550.0
        self.y1 = 550.0
        
        """
        Dado que se conocen previamente los puntos de eventos, introducimos en la cola llamada `self.points` los puntos que hemos indicado.
        Si hay nodos que se encuentran fuera de la caja, es posible que sea necesario modificar las dimensiones de la caja 
        para asegurarnos de que todos los nodos se encuentren dentro de ella. 
        Esto se hace para garantizar que los cálculos y las intersecciones de segmentos se realicen correctamente.
        """

        # insert points to site event
        for pts in points:
            point = Point(pts[0], pts[1])
            self.points.push(point)
            # keep track of bounding box size
            if point.x < self.x0: self.x0 = point.x
            if point.y < self.y0: self.y0 = point.y
            if point.x > self.x1: self.x1 = point.x
            if point.y > self.y1: self.y1 = point.y

        # add margins to the bounding box
        dx = (self.x1 - self.x0 + 1) / 5.0
        dy = (self.y1 - self.y0 + 1) / 5.0
        self.x0 = self.x0 - dx
        self.x1 = self.x1 + dx
        self.y0 = self.y0 - dy
        self.y1 = self.y1 + dy

    def process(self):
        """ 
        Este proceso maneja el movimiento de la línea de barrido mientras se desplaza a través de los eventos.
        A medida que la línea de barrido se desplaza, encuentra nodos y puntos y procesa los eventos asociados a ellos.
        Cuando se han procesado todos los nodos y se ha completado el bucle principal, es posible que no todas las circunferencias
        de eventos hayan ocurrido. Por lo tanto, es necesario continuar procesando esos eventos restantes para asegurarse 
        de que todos los eventos se hayan tenido en cuenta y se haya completado el proceso correctamente.
        Esto asegura que se procesen todos los eventos, incluso aquellos que pueden ocurrir después de que se hayan procesado todos los nodos,
        para garantizar la integridad y completitud del proceso.
        """
        while not self.points.empty():
            """
            Sabiendo que la cola de prioridad de las circunferencias de eventos no está vacía, podemos determinar el orden de procesamiento
            entre las circunferencia de eventos  y los puntos de eventos. Si una circunferencia de eventos ocurre antes que un punto de eventos,
            debemos procesar primero la circunferencia de eventos. Esto implica tomar la circunferencia de eventos de mayor prioridad 
            de la cola de prioridad y realizar las operaciones correspondientes. 
            En caso contrario, si un punto de eventos ocurre antes que un evento de circunferencia, debemos procesar primero el punto de eventos. 
            Esto implica tomar el punto de eventos de mayor prioridad de la cola de prioridad y realizar las operaciones correspondientes.
            """
            if not self.event.empty() and (self.event.top().x <= self.points.top().x):
                self.process_event() # handle circle event
            else:
                self.process_point() # handle site event

        # after all points, process remaining circle events
        while not self.event.empty():
            self.process_event()
        
        """
        Después de procesar todos los eventos, es necesario unir con la caja aquellos segmentos que no han terminado su procesamiento. 
        Esto implica tomar los segmentos que no tienen un punto final definido y extenderlos hasta que se encuentren con los bordes de la caja. 
        De esta manera, se asegura que todos los segmentos estén correctamente conectados y no queden incompletos.
        """

        self.finish_edges()

    def process_point(self):
        """
        Para procesar los eventos, obtenemos el punto de eventos con mayor prioridad de la cola de prioridad. 
        A continuación, eliminamos ese punto de eventos de la cola de prioridad, ya que lo vamos a procesar.
        Insertamos el punto de eventos en el árbol.
        """
        # get next event from site pq
        p = self.points.pop()
        # add new arc (parabola)
        self.arc_insert(p)

    def process_event(self):
        """
        Sacamos el evento de mayor prioridad de la cola de prioridad de eventos. Comprobamos si el evento es válido. 
        Esto es importante para descartar eventos que ya han sido procesados o que no son relevantes para el proceso actual. Si el evento es válido, 
        creamos un segmento que comienza en el punto asignado al evento (el centro de la circunferencia). A continuación, dado que sabemos que 
        el arco asignado 'a' va a ser eliminado, procedemos a conectar 'a.pprev' y 'a.pnext', lo que implica enlazar los arcos vecinos y eliminar el arco 'a'.
        Finalizamos los segmentos relacionados con el arco 'a'. Esto puede implicar extender los segmentos hasta su punto final correspondiente
        o marcarlos como segmentos finalizados, según el caso. Revisamos si las circunferencias de eventos del entorno han sido modificadas.
        Esto implica verificar si ha habido cambios en las circunferencias que afectan a otros eventos pendientes.
        En caso de haber modificaciones, se deben actualizar los eventos relacionados y volver a introducirlos en la cola de 
        prioridad de eventos correspondiente.
        """
        # get next event from circle pq
        e = self.event.pop()

        if e.valid:
            # start new edge
            s = Segment(e.p)
            self.output.append(s)

            # remove associated arc (parabola)
            a = e.a
            if a.pprev is not None:
                a.pprev.pnext = a.pnext
                a.pprev.s1 = s
            if a.pnext is not None:
                a.pnext.pprev = a.pprev
                a.pnext.s0 = s
            
            if self.delau:
                """
                Creamos el triángulo formado por los tres nodos para generar la triangulación de delaunay
                """
                seg_1=Segment(a.p)
                seg_1.done=True
                seg_1.end=a.pprev.p
                self.delaunay.append(seg_1)
                
                seg_2=Segment(a.p)
                seg_2.done=True
                seg_2.end=a.pnext.p
                self.delaunay.append(seg_2)
                
                seg_3=Segment(a.pprev.p)
                seg_3.done=True
                seg_3.end=a.pnext.p
                self.delaunay.append(seg_3)

            # finish the edges before and after a
            if a.s0 is not None: a.s0.finish(e.p)
            if a.s1 is not None: a.s1.finish(e.p)

            # recheck circle events on either side of p
            if a.pprev is not None: self.check_circle_event(a.pprev, e.x)
            if a.pnext is not None: self.check_circle_event(a.pnext, e.x)

    def arc_insert(self, p):
        """
        Si el árbol está vacío, creamos un nuevo árbol. En caso contrario, recorremos el árbol para determinar si la parábola generada por el punto 'p' 
        intersecta con algún arco existente en el árbol.
        """
        if self.arc is None:
            self.arc = Arc(p)
        else:
            # find the current arcs at p.y
            i = self.arc
            while i is not None:
                """
                Primero, comprobamos si la parábola generada por el punto 'p' corta con el arco 'i'. Si 'flag' es False, 
                esto indica que no hay intersección y pasamos al siguiente arco. Si la parábola corta con el arco 'i', procedemos a verificar si también
                corta con el siguiente arco 'i.pnext'. Si hay una intersección con el siguiente arco y este no es nulo, 
                creamos un nuevo arco cuyo foco es 'i.p', con 'i' como arco anterior y 'i.pnext' como arco posterior. Si la condición anterior no se cumple,
                creamos un nuevo arco 'i' que tenga como siguiente arco a 'i.pnext'. A continuación, asignamos los arcos en el siguiente orden: 
                    <'i', 'p', 'i.pnext'>
                De esta manera, hemos pasado de tener <'i', 'i.pnext'> a tener <'i', 'p', 'i.pnext'>.
                Luego, asignamos los segmentos correspondientes a los arcos y los añadimos a la lista de segmentos. Por otra parte, comprobamos
                si las circunferencias de eventos han sido modificadas. En caso de haber modificaciones, se deben actualizar los eventos relacionados y 
                volver a introducirlos en la cola de prioridad de eventos correspondiente.
                """
                flag, z = self.intersect(p, i)
                if flag:
                    # new parabola intersects arc i
                    flag, zz = self.intersect(p, i.pnext)
                    if (i.pnext is not None) and (not flag):
                        i.pnext.pprev = Arc(i.p, i, i.pnext)
                        i.pnext = i.pnext.pprev
                    else:
                        i.pnext = Arc(i.p, i)
                    i.pnext.s1 = i.s1

                    # add p between i and i.pnext
                    i.pnext.pprev = Arc(p, i, i.pnext)
                    i.pnext = i.pnext.pprev

                    i = i.pnext # now i points to the new arc

                    # add new half-edges connected to i's endpoints
                    seg = Segment(z)
                    self.output.append(seg)
                    i.pprev.s1 = i.s0 = seg

                    seg = Segment(z)
                    self.output.append(seg)
                    i.pnext.s0 = i.s1 = seg

                    # check for new circle events around the new arc
                    self.check_circle_event(i, p.x)
                    self.check_circle_event(i.pprev, p.x)
                    self.check_circle_event(i.pnext, p.x)

                    return
                        
                i = i.pnext
            


            # Si p nunca intersecta con algún arco entonces lo añadimos al arbol
            i = self.arc
            while i.pnext is not None:
                i = i.pnext
            i.pnext = Arc(p, i)
            
            # Insertamos el nuevo segmento entre p e i
            x = self.x0
            y = (i.pnext.p.y + i.p.y) / 2.0;
            start = Point(x, y)

            seg = Segment(start)
            i.s1 = i.pnext.s0 = seg
            self.output.append(seg)

    def check_circle_event(self, i, x0):
        """
        Comprobamos si hay una nueva circunferencia de eventos relacionada con el arco 'i'. En algunos casos puede haber una falsa alarma, en ese caso,
        en lugar de eliminar el evento correspondiente, simplemente marcamos el evento como inválido, lo que significa que no se procesará.
        """
        if (i.e is not None) and (i.e.x  !=  self.x0): 
            i.e.valid = False
        i.e = None

        if (i.pprev is None) or (i.pnext is None): return
        
        
        flag, x, o = self.circle(i.pprev.p, i.p, i.pnext.p)
        if flag and (x > self.x0):
            i.e = Event(x, o, i)
            self.event.push(i.e)

    def circle(self, a, b, c):
        """
        Si la circunferencia generada por los tres puntos tiene un centro que está por encima de los tres puntos entonces 
        se devuelve 'false' y sin puntos.
        Para realizar esta verificación, utilizamos el producto vectorial de Gibbs entre los dos vectores que representan la direccion de la mediatrices 
        de dos de los lados del triángulo:

           |   i       j      k   |
           | a.y-b.y  b.x-a.x   0 |
           | a.y-c.y  c.x-a.x   0 |
   
        Donde 'i', 'j' y 'k' representan los vectores unitarios en los ejes x, y, y z respectivamente, y 'a', 'b' y 'c' son los puntos que forman
        la circunferencia.
        El resultado del producto vectorial nos devuelve un vector con tres componentes. En este caso, nos interesa la positividad de la tercera componente.
        Si la tercera componente es positiva, entonces por la regla de la mano derecha los vectores tienen una orientación antihoraria, esto indica que 
        el centro de la circunferencia se encuentra por encima de los tres puntos. Entonces según descienda la línea de barrido las mediatrices van a diverger, 
        por tanto este caso no es una potencial circunferencia de eventos. 
        Por otro lado, si la tercera componente es negativa, esto indica que el centro de la circunferencia se encuentra por
        debajo de los tres puntos. Entonces los vectores tienen una orientación horaria, así que según descienda la línea de barrido 
        aparecerá el punto de convergencia.
        """

        if ((b.x - a.x)*(c.y - a.y) - (c.x - a.x)*(b.y - a.y)) > 0: return False, None, None

        # Joseph O'Rourke, Computational Geometry in C (2nd ed.) p.189
        A = b.x - a.x
        B = b.y - a.y
        C = c.x - a.x
        D = c.y - a.y
        E = A*(a.x + b.x) + B*(a.y + b.y)
        F = C*(a.x + c.x) + D*(a.y + c.y)
        G = 2*(A*(c.y - a.y) - B*(c.x - a.x))
        """
         G es el 2*producto escalar del vector perpendicular a (A,B), el cual une a con b, con el vector (D,-C) perpendicular al vector
        (C,D), que une b con c. Sea   e' =(a+b)/2   f'=(b+c)/2
        
           |x= e'.x + B
        r1=|
           |y= e'.y - A
           
           |x= f'.x + D
        r2=|
           |y= f'.y - C
           
        r1: (A/B) * x + y = (A/B) * e'.x +e'.y
        r2: (D/C) * x + y = (D/C) * f'.x +f'.y
        
        x= (D * (A * e'.x + B * e'.y) - B * (D * f'.x + D * f'.y)/(A*D - B*C)
        y= (A * (C * f'.x + D * f'.y) - C * (A * e'.x + B * f'.y)/(A*D - B*C)
        
        Entonces el procedimiento realizado consiste en trazar dos mediatrizes respecto al triángulo formado por a, b y c y obtener 
        su punto intersección
        """

        if (G == 0): return False, None, None # Points are co-linear

        # point o is the center of the circle
        ox = 1.0 * (D*E - B*F) / G
        oy = 1.0 * (A*F - C*E) / G

        # o.x plus radius equals max x coord
        x = ox + math.sqrt((a.x-ox)**2 + (a.y-oy)**2)
        o = Point(ox, oy)
        
           
        return True, x, o
        
    def intersect(self, p, i):
        """
        Verificamos si el arco 'i' intersecta con el arco de p. Si el arco 'i' intersecta con el arco de p, debemos determinar en qué punto ocurre la intersección.
        """
        # check whether a new parabola at point p intersect with arc i
        if (i is None): return False, None
        if (i.p.x == p.x): return False, None

        a = 0.0
        b = 0.0
        """
        Si el arco anterior a 'i' no es nulo, calculamos la intersección entre el arco 'i' y su arco anterior.
        Obtenemos la componente 'y' de la intersección calculada.
        Realizamos el mismo procedimiento con el arco siguiente a 'i', calculando la intersección entre el arco 'i' y su arco siguiente.
        Obtenemos la componente 'y' de la intersección calculada.
        """

        if i.pprev is not None:
            a = (self.intersection(i.pprev.p, i.p, 1.0*p.x)).y
        if i.pnext is not None:
            b = (self.intersection(i.p, i.pnext.p, 1.0*p.x)).y
        
        """
         Comprobamos las siguientes condiciones:
           Si el arco anterior a 'i' es nulo o el punto 'p' es mayor que el punto de intersección 'a' (en términos de la coordenada 'y') y 
           si el arco posterior a 'i' es nulo o el punto 'p' es menor que el punto de intersección 'b' (en términos de la coordenada 'y')
           
         Entonces realizamos lo siguiente:
           - Mantenemos la coordenada 'y' del punto de intersección correspondiente.
           - Buscamos en el arco 'i' la posición 'x' correspondiente a la posición 'y' del punto 'p'.
        """

        if (((i.pprev is None) or (a <= p.y)) and ((i.pnext is None) or (p.y <= b))):
            py = p.y
            px = 1.0 * ((i.p.x)**2 + (i.p.y-py)**2 - p.x**2) / (2*i.p.x - 2*p.x)
            res = Point(px, py)
            return True, res
        return False, None

    def intersection(self, p0, p1, l):
        # get the intersection of two parabolas
        """
        La fórmula de las parábolas dado un foco (h,k) y una directriz l es:
            Si los puntos de una parábola son 
            sqrt((x - h)** 2+(y - k)** 2) = |x - l| =>
            => (x - h)** 2 + (y - k)** 2 = (x - l)** 2 =>
            => x** 2 + h** 2 -2xh +y** 2 + k**2 -2ky = x**2 + l**2 - 2lx =>
            =>  y** 2 -2ky + k**2 - l**2 + h** 2= (2h - 2l) * x => (y** 2)/(2h - 2l) -(2ky)/(2h - 2l) + (k**2 - l**2 + h** 2)/(2h - 2l) = x
            
            Entonces se extrae fácilmente que de la ecuación general ay**2 + by + c = x
            
            a = 1/(2h - 2l)
            b = -(2k)/(2h - 2l)
            c = (k**2 - l**2 + h** 2)/(2h - 2l)
            
            Con todos esto datos se puede resolver el problema
        """
        p = p0
        if (p0.x == p1.x):
            py = (p0.y + p1.y) / 2.0
        elif (p1.x == l):
            py = p1.y
        elif (p0.x == l):
            py = p0.y
            p = p1
        else:
            # use quadratic formula
            z0 = 2.0 * (p0.x - l)
            z1 = 2.0 * (p1.x - l)

            a = 1.0/z0 - 1.0/z1;
            b = -2.0 * (p0.y/z0 - p1.y/z1)
            c = 1.0 * (p0.y**2 + p0.x**2 - l**2) / z0 - 1.0 * (p1.y**2 + p1.x**2 - l**2) / z1

            py = 1.0 * (-b-math.sqrt(b*b - 4*a*c)) / (2*a)
            
        px = 1.0 * (p.x**2 + (p.y-py)**2 - l**2) / (2*p.x-2*l)
        res = Point(px, py)
        return res

    def finish_edges(self):
        """
        Completamos todos los segmentos cuya componente 'end' es 'None'.
        Definimos 'l' como la recta directriz en el instante en el que se han procesado todos los eventos. 
        Definimos 'i' como el arco actual.
        """
        l = self.x1 + (self.x1 - self.x0) + (self.y1 - self.y0)
        i = self.arc
        while i.pnext is not None:
            if i.s1 is not None:
                """
                Tomamos '2*l' como un valor lo suficientemente lejano para asegurarnos de que la recta se dibuje por completo.
                Encontramos el punto de intersección entre la recta '2*l' y el arco 'i'.
                Añadimos el punto de intersección al segmento correspondiente.
                """
                p = self.intersection(i.p, i.pnext.p, l*2.0)
                i.s1.finish(p)
            i = i.pnext

    def print_output(self):
        it = 0
        for o in self.output:
            it = it + 1
            p0 = o.start
            p1 = o.end
            print (p0.x, p0.y, p1.x, p1.y)
            

    def get_output(self):
        """
        Se guarda en una lista todos los segmentos para representarlos en un futuro
        """
        res = []
        for o in self.output:
            p0 = o.start
            p1 = o.end
            res.append((p0.x, p0.y, p1.x, p1.y))
        return res
    
    def get_del(self):
        """
        Se guarda en una lista todos los segmentos para representarlos en un futuro
        """
        res = []
        for o in self.delaunay:
            p0 = o.start
            p1 = o.end
            res.append((p0.x, p0.y, p1.x, p1.y))
        return res
    
    
    
    