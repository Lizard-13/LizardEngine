#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 4/12/2014 (dd/mm/aa)

import LE.LizardEngine as le
from pygame.locals import QUIT, K_ESCAPE, K_SPACE


# Una escena heredada para definir su comportamiento
class EscenaBasica(le.Escena):
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
escena = EscenaBasica("LizardEngine - Ejemplo Básico")
# Se establece la escena
nucleo.cambiar_escena(escena)
# Se crea una cámara y se definen sus framebuffers
camara = le.Camara(tam=escena.tam)
camara.fbos = [le.Framebuffer(escena.tam)]
# Se establece la camara
escena.capa_base.camaras = [camara]

# Se definen los eventos disponibles
nucleo.mapa_eve.definir_otro(QUIT)
nucleo.mapa_eve.definir_teclas(K_ESCAPE, K_SPACE)

# Se limpian referencias sin uso
escena = None
camara = None

# Se ejecuta el bucle principal
nucleo.ejecutar()