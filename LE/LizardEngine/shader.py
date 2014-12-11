#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 11/10/2014 (dd/mm/aa)

#Globales
import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import *


class Shader():
	def __init__(self,vshader_source,fshader_source):
		self.errores = False
		vshader_file = open(vshader_source,"r")
		fshader_file = open(fshader_source,"r")
		vshader_data = vshader_file.read()
		fshader_data = fshader_file.read()

		vshader = glCreateShader(GL_VERTEX_SHADER)
		fshader = glCreateShader(GL_FRAGMENT_SHADER)
		self.vshader = vshader
		self.fshader = fshader
		self.programa = None

		glShaderSource(vshader, [vshader_data])
		glShaderSource(fshader, [fshader_data])
		vshader_file.close()
		fshader_file.close()
		
		glCompileShader(vshader)
		v_resultado = glGetShaderiv(vshader,GL_COMPILE_STATUS)
		if v_resultado != 1:
			print "Error al compilar el VShader, registro:\n"+glGetShaderInfoLog(vshader)
		glCompileShader(fshader)
		f_resultado = glGetShaderiv(fshader,GL_COMPILE_STATUS)
		if f_resultado != 1:
			print "Error al compilar el FShader, registro:\n"+glGetShaderInfoLog(fshader)
		
		if (v_resultado != 1) or (f_resultado != 1): # error en la compilación
			self.errores = True
			glDeleteShader(fshader)
			glDeleteShader(vshader)
		else:
			self.programa = glCreateProgram()
			glAttachShader(self.programa, vshader)
			glAttachShader(self.programa, fshader)
			try:
				glLinkProgram(self.programa)
				glDetachShader(self.programa, vshader)
				glDetachShader(self.programa, fshader)
			except:
				print 'Error linking program'
				self.errores = True
				glDeleteShader(fshader)
				glDeleteShader(vshader)
				glDeleteProgram(self.programa)

	def usar(self):
		glUseProgram(self.programa)
	
	def no_usar(self):
		glUseProgram(0)
	
	def ubicacion(self, uniforme):
		"""Retorna la ubicación de la vaiable uniforme en el programa.
		uniforme = texto del nombre de la variable"""
		return glGetUniformLocation(self.programa, uniforme)
	
	def parametrizar_textura(self, ubicacion, textura):
		"""Parametriza el shader con una textura (o un int).
		ubicacion = ubicación de la variable a parametrizar
		textura = posición de la textura a través de glActiveTexture()"""
		glUniform1i(ubicacion, textura)
	
	def parametrizar_float(self, ubicacion, valor):
		"""Parametriza el shader con un float
		ubicacion = ubicación de la variable a parametrizar
		valor = valor del flotante"""
		glUniform1f(ubicacion, valor)
	
	def parametrizar_vec2(self, ubicacion, x, y):
		"""Parametriza el shader con un vec2
		ubicacion = ubicación de la variable a parametrizar
		x, y = valores del vector 2D"""
		glUniform3f(ubicacion, x, y)
	
	def parametrizar_vec3(self, ubicacion, x, y, z):
		"""Parametriza el shader con un vec3
		ubicacion = ubicación de la variable a parametrizar
		x, y, z = valores del vector 3D"""
		glUniform3f(ubicacion, x, y, z)
	