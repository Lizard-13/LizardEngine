#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 11/10/2014 (dd/mm/aa)

#Globales
from OpenGL.GL import (glCreateShader, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER,
					   glCreateProgram, glAttachShader, glLinkProgram,
					   glDetachShader, glDeleteShader, glGetProgramiv,
					   GL_LINK_STATUS, glShaderSource, glCompileShader,
					   glGetShaderiv, GL_COMPILE_STATUS, glGetShaderInfoLog,
					   glUseProgram, glGetUniformLocation, glUniform1i,
					   glUniform1f, glUniform2f, glUniform3f, glDeleteProgram)


class Shader():
	def __init__(self, archivo_vert, archivo_frag,
				 nombre_vert="Vertex Shader", nombre_frag="Fragment Shader"):
		print("Shader creado")
		
		# Creación de shaders y programa
		self.vshader = glCreateShader(GL_VERTEX_SHADER)
		self.fshader = glCreateShader(GL_FRAGMENT_SHADER)
		self.programa = glCreateProgram()
		
		# Cargamos los datos de los archivos en los shaders
		self.cargar_datos(self.vshader, archivo_vert)
		self.cargar_datos(self.fshader, archivo_frag)
		# Compilamos los shaders
		resultado_vert = self.compilar(self.vshader, nombre_vert)
		resultado_frag = self.compilar(self.fshader, nombre_frag)
		
		# Error en la compilación
		if (resultado_vert != 1) or (resultado_frag != 1):
			self.destruir()
		# Sin errores hasta ahora
		else:
			# Enlazamos los shaders al programa
			glAttachShader(self.programa, self.vshader)
			glAttachShader(self.programa, self.fshader)
			# Enlazamos el programa
			glLinkProgram(self.programa)
			# Desenlazaos y eliminamos los shaders
			glDetachShader(self.programa, self.vshader)
			glDetachShader(self.programa, self.fshader)
			glDeleteShader(self.vshader)
			glDeleteShader(self.fshader)
			# Errores durante el enlace
			resultado_progr = glGetProgramiv(self.programa, GL_LINK_STATUS)
			if resultado_progr != 1:
				self.destruir()

	def cargar_datos(self, shader, archivo_shader):
		"""Carga el archivo y devuelve los datos del shader.
		shader = shader a cargar los datos
		archivo_shader = archivo con los datos fuente para el shader"""
		# Abrimos el archivo y obtenemos los datos
		archivo = open(archivo_shader,"r")
		data = archivo.read()
		# Cerramos el archivo
		archivo.close()
		# Asignamos los datos al shader
		glShaderSource(shader, [data])
	
	def compilar(self, shader, nombre):
		"""Compila el shader e informa errores.
		shader = shader a compilar
		nombre = nombre del shader en el informe de errores"""
		# Compilamos el shader
		glCompileShader(shader)
		# Obtenemos su estado
		resultado = glGetShaderiv(shader,GL_COMPILE_STATUS)
		# Si el estado es != 1, hubo errores durante la compilación
		if resultado != 1:
			print "Error al compilar {n}, registro:\n".format(n=nombre) + \
					glGetShaderInfoLog(shader)
		# Devolvemos el estado
		return resultado

	def usar(self):
		"""Utilizar este programa."""
		glUseProgram(self.programa)
	
	def ubicacion(self, uniforme):
		"""Retorna la ubicación de la vaiable uniforme en el programa.
		uniforme = texto del nombre de la variable"""
		return glGetUniformLocation(self.programa, uniforme)
	
	def parametrizar_textura(self, ubicacion, textura):
		"""Parametriza el shader con una textura (o un int).
		ubicacion = ubicación de la variable a parametrizar
		textura = posición de la textura a través de glActiveTexture()"""
		glUniform1i(ubicacion, textura)
	
	def parametrizar_decimal(self, ubicacion, valor):
		"""Parametriza el shader con un float
		ubicacion = ubicación de la variable a parametrizar
		valor = valor del flotante"""
		glUniform1f(ubicacion, valor)
	
	def parametrizar_vec2(self, ubicacion, x, y):
		"""Parametriza el shader con un vec2
		ubicacion = ubicación de la variable a parametrizar
		x, y = valores del vector 2D"""
		glUniform2f(ubicacion, x, y)
	
	def parametrizar_vec3(self, ubicacion, x, y, z):
		"""Parametriza el shader con un vec3
		ubicacion = ubicación de la variable a parametrizar
		x, y, z = valores del vector 3D"""
		glUniform3f(ubicacion, x, y, z)
	
	def destruir(self):
		"""Elimina los shaders y el programa, y destruye referencias."""
		glDeleteShader(self.fshader)
		glDeleteShader(self.vshader)
		glDeleteProgram(self.programa)
	
	def __del__(self):
		print("Shader eliminado")
	
	
def no_usar_shaders():
	"""Deja de utilizar cualquier shader."""
	glUseProgram(0)
		