#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 15/12/2014 (dd/mm/aa)

from .shader import Shader


class CajaRecursos(object):
    """Contenedor de recursos varios."""
    def __init__(self):
        """inicializa la caja de recursos"""
        # Por lo general, es posible que hayan demasiadas texturas y sonidos
        # para utilizar diccionarios
        self.texturas = {}
        self.sonidos = {}
        self.shaders = {}
    
    def agregar_textura(self, nombre, imagen):
        """Carga una nueva textura a partir de un archivo.
        nombre = nombre (clave) de la textura
        imagen = archivo de imagen"""
        self.texturas[nombre] = None
    
    def agregar_sonido(self, nombre, sonido):
        """Carga un nuevo sonido a partir de un archivo.
        nombre = nombre (clave) de la textura
        sonido = archivo de sonido"""
        self.sonidos[nombre] = None
    
    def agregar_shader(self, nombre, archivo_vert, archivo_frag):
        """Agrega un nuevo shader a partir de sus archivos.
        nombre = nombre (clave) del shader
        archivo_vert = archivo del Vertex Shader
        archivo_frag = archivo del Fragment Shader"""
        self.shaders[nombre] = Shader(archivo_vert, archivo_frag)
    