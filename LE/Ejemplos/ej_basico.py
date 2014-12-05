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
        
nucleo = le.Nucleo()
escena = EscenaBasica("LizardEngine - Ejemplo Básico")
nucleo.cambiar_escena(escena)
camara = le.Camara(tam=escena.tam)
camara.fbos = [le.Framebuffer(escena.tam)]
escena.capa_base.camaras = [camara]

nucleo.mapa_eve.definir_otro(QUIT)
nucleo.mapa_eve.definir_teclas(K_ESCAPE, K_SPACE)

nucleo.ejecutar()