#!/usr/bin/python
# -*- coding: utf-8 -*-


#Globales
import pygame
from pygame.locals import *
from OpenGL.GL import *

#Locales
from capa import Capa


class Escena():
	"""La escena contiene los objetos, las capas y texturas, ordena la
	actualización de los objetos y capas. Sólo hay una escena activa
	a la vez."""
	def __init__(self, nombre, color=(0.4, 0.4, 0.4),
					   tam=(800, 600), pant_compl=False):
		"""Inicializa la escena.
		nombre = nombre de la escena (título de la ventana por defecto)
		color = color de fondo (de limpiado) de la escena
		tam = tamaño de la ventana de la escena
		pant_compl = ejecutar en pantalla completa"""
		print("Escena creada")
		self.nombre = nombre
		self.color = color
		self.tam = tam
		self.pant_compl = pant_compl
		self.nucleo = None
		self.capas = []
		# Una capa por defecto
		self.capa_base = Capa()
		self.agregar_capa(self.capa_base)
		self.objetos = []
		self.texturas = []
		self.eventos = None

	def actualizar(self, tiempo):
		"""Actualiza la lógica de la escena y llama a actualizar a todos los
		objetos y las capas.
		tiempo = tiempo transcurrido desde el último fotograma"""
		# Ejecutar la lógica de escena
		self.logica(tiempo)
		# Actualizar objetos
		for tipo in self.objetos:
			# Listas de tipo vacias no generan errores (no tienen objetos)
			for objeto in tipo:
				objeto.actualizar(tiempo)
		# Actualizar capas
		for capa in self.capas:
			capa.actualizar(tiempo)

	def logica_ini(self):
		"""Lógica a ejecutar una sola vez al iniciar la escena."""
		pass
			
	def logica(self, tiempo):
		"""Lógica a ejecutar continuamente.
		tiempo = tiempo transcurrido desde el último fotograma"""
		pass

	def renderizar(self):
		"""Llama a renderizar cada capa."""
		for capa in self.capas:
			capa.renderizar()

	def agregar_capa(self, capa, ordenar=True):
		"""Agrega una capa y puede ordenarlas por su valor Z.
		capa = capa a agregar
		ordenar = ordenar las capas (False = No ordenar)"""
		self.capas.append(capa)
		# Dar a la capa información de la escena
		capa.escena = self
		# Ordenar las capas
		if ordenar:
			self.ordenar_capas()

	def ordenar_capas(self):
		"""Ordena las capas por su valor Z."""
		self.capas.sort(key=lambda capa: capa.z)

	def ordenar_objetos(self, capa=None):
		"""Llama a cada capa a ordenar los objetos
		por su valor Z."""
		for capa in self.capas:
			capa.ordenar_objetos()

	def eliminar_capa(self, capa):
		"""Remueve una capa de la lista.
		capa = capa a eliminar"""
		self.capas.remove(capa)

	def visibilidad_capa(self, capa, vis):
		"""Modificar la visibilidad de la capa.
		capa = capa a modificar
		vis = visibilidad (0 = Oculta, 1 = Visible)"""
		pass

	def velocidad_capa(self, capa, vel):
		"""Modificar el reloj interno de la capa.
		capa = capa a modificar
		vel = velocidad (0 = Pausada, 1 = Velicidad normal)"""
		pass

	def agregar_objeto(self, objeto, capa=None):
		"""Agrega un objeto a una capa.
		objeto = objeto a agregar a la capa
		capa = capa a la cual agregar"""
		# Si se agrega un tipo de objeto mayor al tamaño de la lista:
		if len(self.objetos) <= objeto.tipo:
			# Se agregan listas de tipos restantes vacias
			for i in range(objeto.tipo - len(self.objetos) + 1):
				self.objetos.append([])
		# Agregar el objeto en su lista de tipo
		self.objetos[objeto.tipo].append(objeto)
		# Si no se explicita una capa, se usa la capa base
		if not capa:
			capa = self.capa_base
		# Se agrega el objeto a la capa y se ordena
		capa.objetos.append(objeto)
		capa.ordenar_objetos()
		# Se da al objeto información de su capa
		objeto.capa = capa

	def agregar_textura(self, img):
		"""Agrega una textura la lista de la escena a partir de una imagen.
		img = archivo imagen a agregar como textura"""
		# Transformar en imagen legible para OpenGL
		imagen = pygame.image.load(img)
		textura_info = pygame.image.tostring(imagen, "RGBA", 1)
		# Obtener el tamaño
		ancho, alto = imagen.get_size()
		# Crear la textura
		textura = glGenTextures(1)
		# Usarla
		glBindTexture(GL_TEXTURE_2D, textura)
		# Establecer los parámetros (incluyendo la imagen misma)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ancho, alto, 0,
					 GL_RGBA, GL_UNSIGNED_BYTE, textura_info)
		# Agregar la textura
		self.texturas.append(textura)
		

	def cargar_escena(self, archivo):
		"""Carga objetos y recursos de un archivo a través del cargador de
		recursos del núcleo.
		archivo = archivo a cargar"""
		try:
			self.nucleo.cargador.cargar_escena(archivo, self)
		except IOError:
			raise Exception("No se encontró {archivo}".format(archivo=archivo))

	def cambiar_color(self, r, g, b):
		"""Cambia el color del fondo (de limpiado) de la escena.
		r,g,b = canales rojo, verde y azul del color respectivamente"""
		self.color = (r,g,b)
		glClearColor(r,g,b,1.0)
	
	def destruir(self):
		# Elimina referencias para poder eliminarlos
		self.nucleo = None
		self.eventos = None
		self.capa_base = None
		# Destruir objetos para eliminar sus referencias
		for tipo in self.objetos:
			for objeto in tipo:
				objeto.destruir()
		# Destruir capas para eliminar sus referencias
		for capa in self.capas:
			capa.destruir()
		# Al no tener referncias, son eliminados al ser olvidados por la escena
		self.objetos = None
		self.capas = None
		# Limpiar las texturas
		glDeleteTextures(self.texturas)

	def __del__(self):
		print("Escena eliminada")
