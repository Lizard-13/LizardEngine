#!/usr/bin/python
# -*- coding: utf-8 -*-

from Ejemplos import *

print("Versión 1.5")

c = EjemploBasico()
class ControlEjemplos(object):
    """Documentación de la clase"""
    def __init__(self):
        """Documentación de la función"""
        pass
    def CaragarEjemplo(self):
        """Documentación de la función"""
        self.ejemplo = EjemploBasico()


#Prueba inicial del motor
import LizardEngine as le
vec = le.Vec2((5,3))
print(vec)