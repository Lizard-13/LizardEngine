#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 4/12/2014 (dd/mm/aa)

import LE.LizardEngine as le
from pygame.locals import QUIT, K_ESCAPE, K_SPACE
from OpenGL.GL import (glClearColor, glActiveTexture, glBindTexture,
                       glClear, GL_COLOR_BUFFER_BIT, GL_TEXTURE_2D,
                       GL_TEXTURE0, GL_TEXTURE1)


#Carpeta relativa de recursos, archivos en formato recursos%"archivo"
recursos = "Recursos/EjCamara/%s"

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
        """Inicia los parámetros constantes de los shaders."""
        # Variables del blur horizontal
        shader_h.usar()
        shader_h.parametrizar_textura(shader_h.ubicacion("textura"), 0)
        shader_h.parametrizar_float(shader_h.ubicacion("blurH"), 1.0/512.0)
        # Variables del blur vertical
        shader_v.usar()
        shader_v.parametrizar_textura(shader_v.ubicacion("textura"), 1)
        shader_v.parametrizar_float(shader_v.ubicacion("blurV"), 1.0/512.0)
        # Finalizar
        shader_v.no_usar()
    
    def finalizar_renderizado(self):
        """Renderiza la textura final, obtenida en el framebuffer 0."""
        # Desactivar el primer framebuffer y activar el segundo
        self.fbos[1].usar()
        glClearColor(0., 0., 0., 0.)
        glClear(GL_COLOR_BUFFER_BIT)
        # Activar la primer textura
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.fbos[0].textura)
        # Renderiza la imagen principal con el shader de blur horizontal
        self.shader_h.usar()
        self.renderizar_cuad(0., 0., self.ventana[0], self.ventana[1])
        # Desactivar el segundo framebuffer
        self.fbos[1].no_usar()
        glClearColor(0., 0., 0., 0.)
        glClear(GL_COLOR_BUFFER_BIT)
        # Activar la segunda textura con el shader de blur vertical
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.fbos[1].textura)
        # Renderiza a la pantalla utilizando blur vertical
        self.shader_v.usar()
        inicio_x = self.zona[0]*self.ventana[0]
        inicio_y = self.zona[1]*self.ventana[1]
        fin_x = self.zona[2]*self.ventana[0]
        fin_y = self.zona[3]*self.ventana[1]
        self.renderizar_cuad(inicio_x, inicio_y, fin_x, fin_y)
        self.shader_v.no_usar()
        # Pequeño render lateral sin usar el programa (textura del framebuffer)
        glActiveTexture(GL_TEXTURE0)
        self.renderizar_cuad(self.ventana[0]-160, 0., self.ventana[0], 120.)
        glBindTexture(GL_TEXTURE_2D, self.fbos[1].textura)
        self.renderizar_cuad(self.ventana[0]-160, 130., self.ventana[0], 250.)


# Una escena heredada para definir su comportamiento
class EscenaBasica(le.Escena):
    """Escena con lógica."""
    def logica_ini(self):
        # Agregamos una textura
        self.agregar_textura(recursos%"Iori_0.png")
        # Creamos el objeto con dicha textura
        obj = le.ObjetoImagenAvanzado(self.texturas[0], [100,50])
        # Le definimos un grupo
        obj.tipo = 0
        # Lo agrandamos un poco
        obj.escala = le.Vec2((3,3))
        # Agregamos el objeto
        self.agregar_objeto(obj)
        
    def logica(self, tiempo):
        # Eventos del teclado
        teclado = self.eventos.entrada_teclado
        if teclado[K_ESCAPE][0]:
            self.nucleo.salir()
        if teclado[K_SPACE][0]:
            self.color = (80, 200, 80)
        # Eventos varios
        if self.eventos.entrada_otros[QUIT]:
            self.nucleo.salir()

# Se crea el núcleo
nucleo = le.Nucleo()
# Se crea una nueva escena, con lógica definida
escena = EscenaBasica("LizardEngine - Ejemplo de Cámaras")
# Se establece la escena
nucleo.cambiar_escena(escena)
# Se crea una cámara
camara = CamaraBlur([0,0], escena.tam)
# Se establece la camara
escena.capa_base.camaras = [camara]

# Se definen los eventos disponibles
nucleo.mapa_eve.definir_otro(QUIT)
nucleo.mapa_eve.definir_teclas(K_ESCAPE, K_SPACE)

# Se limpian referencias sin uso
del escena# = None
del camara# = None

# Se ejecuta el bucle principal
nucleo.ejecutar()