#!/usr/bin/python
# -* -coding: utf-8 -*-

# Globales
import pygame
from pygame.locals import *
from OpenGL.GL import *
from sys import exit as sys_exit

# Locales
from mapa_evento import MapaEvento
from cargador import Cargador


class Nucleo():
	def __init__(self, tam=(640, 480), fps=60):
		"""Inicializador del nucleo, sin escena, sólo un reloj,
		un mapa de eventos, y una ventana básica.
		tam = dimensiones de la ventana inicial (inútil)
		título = título de la ventana inicial
		fps = fotogramas por segundo máximos"""
		print("Núcleo creado")
		self.mapa_eve = MapaEvento()
		self.cargador = Cargador()
		# Ninguna escena por defecto
		self.escena = None 
		# Ventana inicial e inicio de OpenGL
		print("Iniciando contexto OpenGL...")
		pygame.display.set_mode(tam, DOUBLEBUF | OPENGL)
		pygame.display.set_caption("LizardEngine - Núcleo")
		self.gl_ini(*tam)
		# Reloj principal (delta-tiempo)
		self.reloj = pygame.time.Clock()
		self.fps = fps
		if self.fps <= 0:
			self.fps = 60

	def gl_ini(self, v_ancho, v_alto):
		"""Inicia las opeciones de OpenGL con un tamaño de
		ventana dado, por defecto OpenGL utiliza toda la ventana.
		v_ancho, v_alto = dimensiones de la ventana"""
		# Projección de OpenGL
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, v_ancho, v_alto, 0, 0, 1)
		glViewport(0, 0, v_ancho, v_alto)
		glMatrixMode(GL_MODELVIEW)
		# Opciones tipo
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glEnable(GL_ALPHA_TEST)
		glEnable(GL_TEXTURE_2D)
		glDisable(GL_DEPTH_TEST)
		glClearColor(0.0, 0.0, 0.0, 1.0)
		glPointSize(4)

	def actualizar(self):
		"""Actualiza el reloj, así como llama a
		actualizar a la escena actual y los eventos."""
		self.reloj.tick()#self.fps)
		tiempo = self.reloj.get_time() / 1000.0
		# Chequeo inicial de eventos
		self.mapa_eve.actualizar_i()
		# Actualización de la escena
		self.escena.actualizar(tiempo)
		# Doble cheuqeo, para detetar eventos activados por primera vez
		self.mapa_eve.actualizar_f()

	def renderizar(self):
		"""LLama a renderizar la escena actual."""
		# Limpiar la pantalla
		glClear(GL_COLOR_BUFFER_BIT)
		# Renderizar la escena
		self.escena.renderizar()
		# Renderizar los buffers a la pantalla
		pygame.display.flip()

	def cambiar_escena(self, escena):
		"""Cambia la escena actual por una nueva dada, todos los datos de la
		escena se pierden.
		escena = escena a cambiar"""
		# Reemplazo directo
		self.escena = escena
		# Reiniciar la ventana con el tamaño de la nueva escena
		print("Iniciando nuevo contexto OpenGL...")
		v_ancho, v_alto = escena.tam
		opciones = OPENGL | DOUBLEBUF
		if escena.pant_compl:
			opciones |= FULLSCREEN
		pygame.display.set_mode((v_ancho, v_alto), opciones)
		# Título por defecto de la ventana
		pygame.display.set_caption(escena.nombre)
		# Reiniciar OpenGL
		self.gl_ini(v_ancho, v_alto)
		# Darle los datos del núcleo a la ventana
		self.escena.nucleo = self
		self.escena.eventos = self.mapa_eve
		self.escena.cambiar_color(*escena.color)
		# Ejecutar la lógica inicial de la escena
		print("Iniciando escena...")
		self.escena.logica_ini()

	def definir_mapa_evento(self, mapa_evento):
		"""Define que mapa de eventos usará el núcleo.
		mapa_evento = nuevo mapa de eventos a utilizar"""
		# Reemplazo directo
		self.mapa_eve = mapa_evento
		# Si el núcleo ya tiene escena, actualizarla también
		if self.escena:
			self.escena.eventos = self.mapa_eve

	def ejecutar(self):
		"""Inicia el bucleo principal del núcleo."""
		while True:
			self.actualizar()
			self.renderizar()

	def salir(self):
		"""Finaliza los objetos y pygame, y cierra la aplicaión."""
		# Eliminar las referencias de la escena
		self.escena.destruir()
		# Al no tener referencias, son eliminados al ser olvidados por el núcleo
		self.escena = None
		self.mapa_eve = None
		self.reloj = None
		# Finalizar Pygame y cerrar la aplicaión
		pygame.quit()
		sys_exit()

	def __del__(self):
		print("Núcleo eliminado")
