#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 8/07/2014 (dd/mm/aa)


class Vec2():
	"""Objeto que representa un vector en 2D."""
	def __init__(self, lista=None, vec2=None, x=None,y=None):
		"""Inicializa el vector.
		lista = inicia el vector a partir de una lista [x,y]
		vec2 = inicia el vector a partir de otro Vec2
		x,y = inicia el vector directamente con sus dos valores"""
		if lista:
			self.x, self.y = lista
		elif vec2:
			self.x, self.y = vec2.x, vec2.y
		elif x and y:
			self.x, self.y = x, y
			
	def __add__(self, vec2):
		"""Retorna un nuevo vector suma de dos vectores.
		vec2 = vector a sumar"""
		return Vec2((self.x+vec2.x, self.y+vec2.y))
	
	def __sub__(self, vec2):
		"""Retorna un nuevo vector resta de dos vectores.
		vec2 = vector a restar"""
		return Vec2((self.x-vec2.x, self.y-vec2.y))
	
	def __mul__(self, k):
		"""Retorna un nuevo vector multiplicado por una constante.
		k = escalar a multiplicar"""
		return Vec2((self.x*k, self.y*k))
	
	def __getitem__(self, item):
		"""Retorna los valores x,y a partir de los índices 0,1 respectivamente.
		item = item del vector (0 ó 1)"""
		return self.lista[item]
	
	def __repr__(self):
		"""Representación literal del vector."""
		return "Vec2({self.x:.3f}, {self.y:.3f})".format(self=self)
	
	def modulo(self):
		"""Retorna el módulo (largo/norma) del vector."""
		# En base a timeit(), velocidad: **0.5 > sqrt() 
		n = (self.x**2 + self.y**2)
		return n**0.5
	
	def lista(self):
		"""Retorna una lista que representa el vector."""
		return (self.x, self.y)
	
	def entero(self):
		"""Retorna una lista que representa el vector, con números enteros."""
		return (int(self.x), int(self.y))
