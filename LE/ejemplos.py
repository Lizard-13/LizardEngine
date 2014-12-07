#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 3/12/2014 (dd/mm/aa)

import pygame
from Ejemplos import Ejemplo, recursos_ejemplos
from sys import exit as sys_exit


# Futura lista de instancias
lista_ejemplos = []
# Posición (índice) de la imagen del ejemplo, número ejemplos por fila/columna
x, y = 0, 0
n = 4
# Tamaño de la imagen, márgenes iniciales y entre ejemplos
ancho, alto = 160, 120
margen_ini_x, margen_ini_y = 40, 30
margen_x, margen_y = 20, 20
# Orden de los ejemplos, orden vertical si es Falso
orden_horizontal = True

# Crear una lista de instancias de ejemplos, posicionadas en grilla
for recurso in recursos_ejemplos:
    # La posición se calcula a partir de los índices, el tamaño y margen
    if orden_horizontal:
        pos_x = margen_ini_x + x*ancho + x*margen_x
        pos_y = margen_ini_y + y*alto + y*margen_y
    # El orden inverso se obtiene simplemente intercambiando los índices x e y
    else:
        pos_x = margen_ini_x + y*ancho + y*margen_x
        pos_y = margen_ini_y + x*alto + x*margen_y
    # Se crean las instancias
    lista_ejemplos.append(Ejemplo(recurso[0], recurso[1],
                                 (pos_x, pos_y), (ancho, alto)))
    # Se actualizan los índices
    x += 1
    if x >= n:
        x = 0; y += 1
    
    
def iniciar(tam):
    """Inicia la ventana de ejemplos.
    tam = tamaño de la ventana"""
    pantalla = pygame.display.set_mode(tam)
    # Controlador del bucle
    ejecutar = True
    while ejecutar:
        # Limpiar la pantalla
        pantalla.fill((30,30,30))
        # Eventos
        for evento in pygame.event.get():
            # Eventos de cierre
            if evento.type == pygame.QUIT:
                ejecutar = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutar = False
            # Eventos de ratón
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Clic izquierdo
                if evento.button == 1:
                    # Sobre algún ejemplo
                    for ej in lista_ejemplos:
                        if ej.colision_punto(evento.pos):
                            # Ejecuta el ejemplo
                            ej.ejecutar()
        # Renderizar los ejemplos
        for ej in lista_ejemplos:
            ej.renderizar(pantalla)
        # Actualizar la pantalla
        pygame.display.flip()


if __name__ == '__main__':
    iniciar((800,600))
    # Cuando se termina el ejemplo, cerrar todo
    pygame.quit()
    sys_exit()