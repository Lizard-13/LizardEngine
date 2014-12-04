#!/usr/bin/python
# -*- coding: utf-8 -*-

# import LizardEngine as le
from Ejemplos.__ejemplo__ import Ejemplo


class EjCamara(Ejemplo):
    """Ejemplo que muestra posibilidades del uso de las cámaras."""
    def __init__(self):
        """Inicializa el ejemplo con la imagen adecuada."""
        super(EjCamara, self).__init__("EjCamara/ejemplo.png")
        
    def ejecutar(self):
        """Inicia el ejemplo."""
        pass
