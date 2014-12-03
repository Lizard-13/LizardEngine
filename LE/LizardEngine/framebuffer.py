#/usr/bin/python
# -*- coding: utf-8 -*-

#Globales
from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GL.framebufferobjects import *


class Framebuffer(object):
    """Simple framebuffer"""
    def __init__(self, tam):
        """Se genera una textura (del tamaño dado) de color y un Renderbuffer
        de profundidad (del mismo tamaño) por defecto.
        tam = tamaño de la textura"""
        self.tam = tam
        # Textura para el framebuffer
        self.textura = glGenTextures(1)
        print("FBO creado", self.textura)
        glBindTexture(GL_TEXTURE_2D, self.textura)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, self.tam[0], self.tam[1], 0,
                     GL_BGRA, GL_UNSIGNED_BYTE, None)
        # El framebuffer
        self.framebuffer = glGenFramebuffers(1)
        # Enlazar la textura al framebuffer
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,
                               GL_TEXTURE_2D, self.textura, 0)
        # El renderbuffer
        self.renderbuffer = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.renderbuffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24,
                              self.tam[0], self.tam[1])
        # Enlazar el renderbuffer al framebuffer
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT,
                                  GL_RENDERBUFFER, self.renderbuffer)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)

    def __del__(self):
        """Elimina los recursos usados por el framebuffer."""
        print("FBO eliminado")
        glDeleteTextures(self.textura)
        glDeleteRenderbuffers(1, [self.renderbuffer])
        glDeleteFramebuffers(1, [self.framebuffer])
