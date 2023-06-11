# -*- coding: utf-8 -*-
"""
Created on Wed May 17 14:07:35 2023

@author: Alex b
"""
import heapq
import itertools

"""Se crea una clase punto para manejar mejor los datos"""
class Point:
   """
   Clase para representar un punto en el plano
   """
   x = 0.0
   y = 0.0
   
   def __init__(self, x, y):
       self.x = x
       self.y = y
   def __str__(self):
       return f"({self.x},{self.y})"


class Event:
    """
    Clase para representar un evento
    'x' representa el radio de la circunferencia
    'p' representa el centro de la circunferencia
    'a' representa el arco que corresponde el evento
    """
    x = 0.0
    p = None
    a = None
    valid = True
    
    def __init__(self, x, p, a):
        self.x = x
        self.p = p
        self.a = a
        self.valid = True



class Arc:
    """
    Clase para representar un arco de la línea de playa
    'p' representa el nodo que genera el arco
    'pprev' representa  el arco previo,
    'pnext' representa el arco siguiente
    'e' representa el evento que tiene relación con el arco
    's0' representa al segmento que se genera entre el arco y 'pprev'
    's1' representa al segmento que se genera entre el arco y 'pnext'
    """
    p = None
    pprev = None
    pnext = None
    e = None
    s0 = None
    s1 = None
    
    def __init__(self, p, a=None, b=None):
        self.p = p
        self.pprev = a
        self.pnext = b
        self.e = None
        self.s0 = None
        self.s1 = None


class Segment:
    """
    Clase para representar un segmento del diagrama de Voronoi
    'start' representa el comienzo del segmento
    'end' representa el final del segmento
    'done' representa si ha finalizado el segmento
    """
    start = None
    end = None
    done = False
    
    def __init__(self, p):
        self.start = p
        self.end = None
        self.done = False

    def finish(self, p):
        if self.done: return
        self.end = p
        self.done = True 
    
    def __str__(self):
        return f"({self.start},{self.end})"


class PriorityQueue:
    """
    Clase para representar una cola de prioridad
    'push' para introducir elementos en la cola de prioridad
    'top'  para obtener el elemento con mayor prioridad de la cola de prioridad
    'pop'  para obtener el elemento con mayor prioridad y eliminarlo de la cola de prioridad
    'empty' para conocer si la cola de prioridad está vacía
    """
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.counter = itertools.count()

    def push(self, item):
        # check for duplicate
        if item in self.entry_finder: return
        count = next(self.counter)
        # use x-coordinate as a primary key (heapq in python is min-heap)
        entry = [item.x, count, item]
        self.entry_finder[item] = entry
        heapq.heappush(self.pq, entry)

    def remove_entry(self, item):
        entry = self.entry_finder.pop(item)
        entry[-1] = 'Removed'

    def pop(self):
        while self.pq:
            priority, count, item = heapq.heappop(self.pq)
            if item is not 'Removed':
                del self.entry_finder[item]
                return item
        raise KeyError('pop from an empty priority queue')

    def top(self):
        while self.pq:
            priority, count, item = heapq.heappop(self.pq)
            if item is not 'Removed':
                del self.entry_finder[item]
                self.push(item)
                return item
        raise KeyError('top from an empty priority queue')

    def empty(self):
        return not self.pq
            