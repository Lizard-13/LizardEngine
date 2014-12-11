#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 4/12/2014 (dd/mm/aa)

import pygame
import os
import subprocess


class Ejemplo(object):
    """Puede ejecutar un ejemplo al ser llamado"""
    def __init__(self, archivo, imagen, pos, tam):
        """Inicializa el ejemplo
        archivo = archivo a ejecutar como subproceso
        imagen = imagen que representa el ejemplo
        pos = posición de la imagen
        tam = tamaño de la representación"""
        self.dir = os.path.dirname(__file__)
        self.archivo = os.path.join(self.dir, archivo)
        ruta_imagen = os.path.join(self.dir, imagen)
        self.imagen_maestra = pygame.image.load(ruta_imagen)
        self.imagen = pygame.transform.scale(self.imagen_maestra, tam)
        self.pos = pos
        self.tam = tam
    
    def renderizar(self, superficie):
        """Previsualiza el ejemplo con una imagen.
        superficie = superficie sobre la cual dibujar"""
        superficie.blit(self.imagen, self.pos)
    
    def ejecutar(self):
        """Inicia el ejemplo a través de un subproceso, ejecutando el archivo
        mismo del ejemplo."""
        subprocess.Popen(["python", self.archivo], cwd=self.dir)
    
    def colision_punto(self, punto):
        """Verifica si el punto dado está sobre la imagen del ejemplo.
        punto = punto a verificar"""
        if self.pos[0] <= punto[0] <= self.pos[0]+self.tam[0] and \
           self.pos[1] <= punto[1] <= self.pos[1]+self.tam[1]:
            return True

    