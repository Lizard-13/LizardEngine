#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 8/07/2014 (dd/mm/aa)


class Vec2():
	def __init__(self, lista):
		self.x = lista[0]
		self.y = lista[1]
	def __add__(self, vec2):
		return Vec2((self.x+vec2.x, self.y+vec2.y))
	def __sub__(self, vec2):
		return Vec2((self.x-vec2.x, self.y-vec2.y))
	def __mul__(self, k):
		return Vec2((self.x*k, self.y*k))
	def __getitem__(self, item):
		return self.lista[item]
	def __repr__(self):
		return "Vec2(%.3f, %.3f)" %(self.x, self.y)
	def prod_vect(self, vec2):
		return Vec2((self.x*vec2.x, self.y*vec2.y))
	def lista(self):
		return (self.x, self.y)
	def entero(self):
		return (int(self.x),int(self.y))
