#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 8/07/2014 (dd/mm/aa)

# Globales
import pygame
from OpenGL.GL import *


class Capa():
	"""La capa tiene la función de separar diferentes grupos de objetos para
	ser renderizados en un orden y con cámaras específicos."""
	def __init__(self, z=0):
		"""Inicializa la capa.
		z = valor Z (orden de renderizado) de la capa"""
		print("Capa creada")
		self.z = z
		self.escena = None
		self.objetos = []
		# Hay que agregar cámaras al iniciar
		self.camaras = []

	def ordenar_camaras(self):
		"""Ordena las cámaras por su valor Z."""
		self.camaras.sort(key=lambda camara: camara.z)

	def ordenar_objetos(self):
		"""Ordena los objetos por su valor Z."""
		self.objetos.sort(key=lambda objeto: objeto.z)

	def actualizar(self, tiempo):
		"""Actualiza la cámara.
		tiempo = tiempo transcurrido desde el último fotograma"""
		for camara in self.camaras:
			camara.actualizar(tiempo)

	def renderizar(self):
		"""Llama a renderizar a cada cámara, y a cada objeto por cámara."""
		# Renderizar cada cámara
		for camara in self.camaras:
			# Activar framebuffers de cámara (si tiene)
			camara.iniciar_renderizado()
			# Renderizar cada objeto
			for objeto in self.objetos:
				objeto.renderizar(camara)
			# Renderizar framebuffers a la pantalla
			camara.finalizar_renderizado()

	def agregar_camara(self, camara):
		"""Agrega una cámara a la capa.
		camara = cámara a agregar"""
		self.camaras.append(camara)
		# Darle a la cámara información sobre la capa
		camara.capa = self
	
	def destruir(self):
		# Eliminar referencias para que la escena pueda destruir la capa
		self.escena = None
		# Eliminar las referencias de las cámaras
		for camara in self.camaras:
			camara.destruir()
		# Al no tener referncias, son eliminadas al ser olvidadas por la capa
		self.camaras = None
		# Los objetos serán destruidos por la escena
		self.objetos = None

	def __del__(self):
		print("Capa eliminada")
