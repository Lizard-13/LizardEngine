#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 4/12/2014 (dd/mm/aa)

# Locales
import LizardEngine as le

#Globales
import pygame
from pygame.locals import QUIT, K_ESCAPE, K_SPACE
from OpenGL.GL import (glActiveTexture, glBindTexture, GL_TEXTURE_2D,
                       GL_TEXTURE0)


#Carpeta relativa de recursos, archivos en formato recursos%"archivo"
recursos = "Recursos/EjCamara/%s"
recursos_com = "Recursos/Comunes/%s"

# Cámara heredada para definir comportamiento
class CamaraBlur(le.Camara):
    """Cámara que utiliza dos framebuffers para generar blur."""
    def __init__(self, pos, tam):
        """Inicia creando los shaders y framebuffers.
        pos = posición (esquina superior izquierda) de la cámara
        tam = tamaño de la cámara"""
        super(CamaraBlur, self).__init__(pos, tam)
        # Shader del blur horizontal
        self.shader_h = le.Shader(recursos%"Camara.vert",
                                  recursos%"Camara_h.frag")
        # Framebuffer del blur horizontal
        self.fbos.append(le.Framebuffer(self.ventana))
        # Shader del blur vertical
        self.shader_v = le.Shader(recursos%"Camara.vert",
                                  recursos%"Camara_v.frag")
        # Framebuffer del blur vertical
        self.fbos.append(le.Framebuffer(self.ventana))
        # Definir las variables de los shaders
        self.definir_shaders(self.shader_h, self.shader_v)
    
    def definir_shaders(self, shader_h, shader_v):
        """Inicia los parámetros constantes de los shaders.
        shader_h = shader del blur horizontal
        shader_v = shader del blur vertical"""
        # Variables del blur horizontal
        shader_h.usar()
        shader_h.parametrizar_textura(shader_h.ubicacion("textura"), 0)
        shader_h.parametrizar_decimal(shader_h.ubicacion("blurH"), 1.0/512.0)
        # Variables del blur vertical
        shader_v.usar()
        shader_v.parametrizar_textura(shader_v.ubicacion("textura"), 1)
        shader_v.parametrizar_decimal(shader_v.ubicacion("blurV"), 1.0/512.0)
        # Finalizar
        le.no_usar_shaders()
    
    def finalizar_renderizado(self):
        """Renderiza la textura final, obtenida en el framebuffer 0."""
        self.renderizar_por_pasos(True,
                            (0, self.shader_h, self.fbos[0], self.fbos[1]),
                            (1, self.shader_v, self.fbos[1], None))
        
        # Pequeño render lateral sin usar el programa (textura del framebuffer)
        glActiveTexture(GL_TEXTURE0)
        self.renderizar_cuad(self.ventana[0]-160, 0., self.ventana[0], 120.)
        glBindTexture(GL_TEXTURE_2D, self.fbos[1].textura)
        self.renderizar_cuad(self.ventana[0]-160, 130., self.ventana[0], 250.)


i=0
# Una escena heredada para definir su comportamiento
class EscenaBasica(le.Escena):
    """Escena con lógica."""
    def logica_ini(self):
        # Agregamos una textura
        self.agregar_textura(recursos_com%"Iori_0.png")
        # Creamos el objeto con dicha textura
        for i in range(1000):
            n = int(i/100.)
            obj = le.ObjetoImagenAvanzado("Iori"+str(n), self.texturas[0],
                                          [5*(i%100), 50*n])
            # Lo agrandamos un poco
            obj.escala = le.Vec2((2,2))
            # Agregamos el objeto
            self.agregar_objeto(obj)
        
    def logica(self, tiempo):
        global i
        i += 1
        if i%25 == 0:
            pygame.display.set_caption(self.nombre+" FPS: "+str(1/tiempo))
        # Eventos del teclado
        teclado = self.eventos.entrada_teclado
        if teclado[K_ESCAPE][0]:
            self.nucleo.salir()
        if teclado[K_SPACE][0]:
            self.color = (80, 200, 80)
        # Eventos varios
        if self.eventos.entrada_otros[QUIT]:
            self.nucleo.salir()
        
        for obj in self.objetos["Iori1"]:
            pass

# Se crea el núcleo
nucleo = le.Nucleo()
# Se crea una nueva escena, con lógica definida
escena = EscenaBasica("LizardEngine - Ejemplo de Cámaras")
# Se establece la escena
nucleo.cambiar_escena(escena)
# Se crea una cámara
camara = CamaraBlur([0,0], escena.tam)
# Se establece la camara
escena.capas["Base"].agregar_camara(camara)

# Se definen los eventos disponibles
nucleo.mapa_eve.definir_otro(QUIT)
nucleo.mapa_eve.definir_teclas(K_ESCAPE, K_SPACE)

# Se limpian referencias sin uso
del escena# = None
del camara# = None

# Se ejecuta el bucle principal
nucleo.ejecutar()
