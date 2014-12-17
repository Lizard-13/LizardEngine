#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 4/12/2014 (dd/mm/aa)

import LizardEngine as le
from pygame.locals import QUIT, K_ESCAPE, K_SPACE


# Carpeta relativa de recursos, archivos en formato recursos%"archivo"
recursos = "Recursos/EjBasico/%s"
recursos_com = "Recursos/Comunes/%s"

# Una escena heredada para definir su comportamiento
class EscenaBasica(le.Escena):
    """Escena con lógica."""
    def logica_ini(self):
        """Lógica inicial de la escena."""
        # Agregamos una textura
        self.agregar_textura(recursos_com%"Iori_0.png")
        # Creamos el objeto con dicha textura
        obj = le.ObjetoImagenAvanzado("Iori", self.texturas[0], [100,50])
        # Le definimos un grupo
        obj.tipo = 0
        # Lo agrandamos un poco
        obj.escala = le.Vec2((3,3))
        # Agregamos el objeto
        self.agregar_objeto(obj)

    def logica(self, tiempo):
        """Lógica continua de la escena.
        tiempo = tiempo transcurrido desde el último fotograma"""
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
escena = EscenaBasica("LizardEngine - Ejemplo Básico")
# Se establece la escena
nucleo.cambiar_escena(escena)
# Se crea una cámara y se definen sus framebuffers
camara = le.Camara(tam=escena.tam)
camara.fbos = [le.Framebuffer(escena.tam)]
# Se establece la camara
escena.capas["Base"].camaras = [camara]

# Se definen los eventos disponibles
nucleo.mapa_eve.definir_otro(QUIT)
nucleo.mapa_eve.definir_teclas(K_ESCAPE, K_SPACE)

# Se limpian referencias sin uso
del escena# = None
del camara# = None

# Se ejecuta el bucle principal
nucleo.ejecutar()