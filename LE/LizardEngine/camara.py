#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 8/07/2014 (dd/mm/aa)

# Globales
import pygame
from OpenGL.GL import *

# Locales
from .vec2 import Vec2


class Camara(object):
    """Simple cámara"""
    def __init__(self, pos=[0, 0], tam=[640, 480], zona=[0, 0, 1, 1]):
        """Inicializa la cámara.
        pos = posición (esquina superior izquierda) de la cámara
        tam = tamaño de la cámara
        zona = que parte de la ventana ocupará la cámara"""
        print("Cámara creada")
        self.pos = Vec2(pos)
        self.tam = tam
        self.zona = zona
        self.acerc = 1.
        self.angulo = 0.
        self.capa = None
        # Programa
        self.shader = None
        # Tamaño de toda la ventana, para crear fácilmente los framebuffers
        pantalla_inf = pygame.display.Info()
        self.ventana = (pantalla_inf.current_w, pantalla_inf.current_h)
        # Hay que crear framebuffers al iniciar
        self.fbos = []

    def actualizar(self, tiempo):
        """Acciones a repetir continuamente"""
        pass

    def iniciar_renderizado(self):
        """Acciones posteriores al renderizado de objetos."""
        self.fbos[0].usar()
        glClearColor(0., 1., 0., 0.)#0.) para fondo transparente
        glClear(GL_COLOR_BUFFER_BIT) #| GL_DEPTH_BUFFER_BIT)
        # Transformación de la cámara
        glLoadIdentity()
        glScalef(self.acerc, self.acerc, 0.)
        glTranslatef(-self.pos.x, -self.pos.y, 0.)
        glRotatef(-self.angulo*3.14159/180., 0., 0., 1.)

    def usar_programa(self, shader):
        """Al iniciar el programa, establecer la textura
        programa = programa a utilizar."""
        self.shader = shader
        self.shader.usar()
        shader.parametrizar_textura(shader.ubicacion("textura"), 0)
        self.shader.no_usar()

    def finalizar_renderizado(self):
        """Renderiza la textura final, obtenida en el framebuffer."""
        # Desactivar el framebuffer
        self.fbos[0].no_usar()
        # Activar la textura
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.fbos[0].textura)
        # Renderiza la imagen principal
        self.shader.usar() if self.shader else None
        self.renderizar_cuad(0., 0., self.tam[0], self.tam[1])
        self.shader.no_usar if self.shader else None
        # Pequeño render sin usar el programa (textura del framebuffer)
        #self.renderizar_cuad(0., 0., 160., 120.)

    def renderizar_cuad(self, x, y, ancho, alto):
        """Renderiza un cuadrado, se ingresan coordenadas para
        textura por defecto.
        x, y = posición (superior izquierda) del cuadrado
        ancho, alto = tamaño del cuadrado"""
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x, y, 0.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x, alto, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(ancho, alto, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(ancho, y, 0.0)
        glEnd()

    def destruir(self):
        # Elimina referencias para poder ser eliminada por la capa
        self.capa = None
        # El framebuffer no tiene referencias, no es necesario detruir()
        self.fbos = None

    def __del__(self):
        print("Camara eliminada")
