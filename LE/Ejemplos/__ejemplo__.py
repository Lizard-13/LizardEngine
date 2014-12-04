#!/usr/bin/python
# -*- coding: utf-8 -*-


class Ejemplo(object):
    """Puede ejecutar un ejemplo al ser llamado"""
    def __init__(self, imagen):
        """Inicializa el ejemplo"""
        self.imagen = imagen
        
    def ejecutar(self):
        """Inicia el ejemplo."""
        pass
    
    def renderizar(self):
        """Previsualiza el ejemplo con una imagen."""
        print self.imagen
