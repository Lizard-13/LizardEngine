#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 10/07/2014 (dd/mm/aa)


#Globales
from OpenGL.GL import *

#Locales
from objeto_base import ObjetoImagen
from vec2 import Vec2


class ObjetoAnimado(ObjetoImagen):
	"""Objeto de renderizado avanzado, con multiples animaciones."""
	def __init__(self, pos=(0,0), z=0):
		"""Inicializa el objeto.
		pos = posición (respecto al punto origen del fotograma) del objeto
		z = valor Z (orden de renderizado) del objeto"""
		ObjetoImagen.__init__(self, pos, z)
		self.anims = []
		self.anim_actual = None

	def renderizar(self, camara):
		"""Renderiza el objeto"""
		# Obtener el fotograma actual, los puntos, textura y tamaño
		ftgr = 	self.ftgr_actual()
		puntos = ftgr.puntos
		textura = ftgr.textura
		tam = ftgr.tam
		# Renderizado
		ObjetoImagen.renderizar(self, puntos, textura, tam, camara)
		# Renderizado de prueba (puntos)
		#self.renderizado_de_prueba()

	def renderizado_de_prueba(self):
		"""Renderizado de puntos para verificar posiciones."""
		puntos = self.ftgr_actual().puntos
		ObjetoImagen.renderizado_de_prueba(self, puntos)

	def accion_activa(self, tiempo):
		"""Funciones de alto consumo. Por defecto, el objeto actualiza su
		animación.
		tiempo = tiempo transcurrido desde el último fotograma"""
		# Debe ser llamada al reescribirse accion_activa() en la herencia
		self.anim_actual.actualizar(tiempo)

	def ftgr_actual(self):
		"""Retorna el fotograma actual de la animación."""
		anim = self.anim_actual
		return anim.ftgrs[anim.ftgr_actual]
		
	def agregar_anim(self, anim):
		"""Agrega una animación al objeto.
		anim = animación a agregar"""
		self.anims.append(anim)
	
	def __del__(self):
		print("Objeto Animado eliminado")


class Animacion():
	"""Objeto que ordena un grupo de fotogramas para producir la animación."""
	def __init__(self, tpf=0.1, bucle=True):
		"""Inicializa el objeto animación.
		tpf = tiempo por fotograma
		bucle = repetir animación al terminar"""
		self.tpf = tpf
		self.bucle = bucle
		self.salto = 1
		self.ftgrs = []
		self.ftgr_actual = 0
		self.t = 0.0

	def actualizar(self, tiempo):
		"""Controla el flujo de la animación.
		tiempo = tiempo transcurrido desde el último fotograma"""
		self.t += tiempo
		# Se ha superado el tpf, actualizar fotograma
		if self.t >= self.tpf:
			self.ftgr_actual += self.salto
			largo = len(self.ftgrs)
			# La animación avanza y ha terminado
			if self.ftgr_actual >= largo:
				if self.bucle:
					self.ftgr_actual -= largo
				else:
					self.ftgr_actual = largo-1
			# La animación retrocede y ha terminado
			elif self.ftgr_actual < 0:
				if self.bucle:
					self.ftgr_actual += largo
				else:
					self.ftgr_actual = 0
			# En caso de que el tiempo se haya excedido,
			# no reiniciamos el t, restamos la velocidad
			self.t -= self.tpf

	def agregar_ftgr(self, ftgr):
		"""Agrega un fotograma a la animación.
		ftgr = fotograma a agregar"""
		self.ftgrs.append(ftgr)


class Fotograma():
	"""Simple objeto que consta de una textura y puntos para ser renderizado."""
	def __init__(self, textura):
		"""Inicializa el fotograma.
		textura = textura del fotograma"""
		self.textura = textura
		# Obtener el tamaño de la textura
		glActiveTexture(GL_TEXTURE0)
		glBindTexture(GL_TEXTURE_2D, self.textura)
		self.tam = (glGetTexLevelParameterfv(GL_TEXTURE_2D, 0,  GL_TEXTURE_WIDTH),
					glGetTexLevelParameterfv(GL_TEXTURE_2D, 0,  GL_TEXTURE_HEIGHT))
		# Establecer los puntos del fotograma
		self.puntos = {"origen": Vec2((0,0)),
					   "centro": Vec2((self.tam[0], self.tam[1])) * 0.5,
					   "rotor" : Vec2((self.tam[0], self.tam[1])) * 0.5}
