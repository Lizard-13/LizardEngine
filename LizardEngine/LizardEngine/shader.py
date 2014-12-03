# -*- coding: utf-8 -*-

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

	def use(self):
		glUseProgram(self.programa)