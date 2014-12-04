#!/usr/bin/python
# -*- coding: utf-8 -*-

# import LizardEngine as le
from Ejemplos.__ejemplo__ import Ejemplo


class EjBasico(Ejemplo):
    """Ejemplo básico para verificar la funcionalidad mínima del motor."""
    def __init__(self):
        """Inicializa el ejemplo con la imagen adecuada."""
        super(EjBasico, self).__init__("EjBasico/ejemplo.png")
        
    def ejecutar(self):
        """Inicia el ejemplo."""
        pass
