#!/usr/bin/env python
# -*- coding: utf-8 -*-
# creado: 8/07/2014 (dd/mm/aa)

#-------------------------------------------------------------------------------
# Nombre:        LizardEngine
#
# Propósito:     LizardEngine planea ser en un futuro un motor
#                  	básico para crear videojuegos en 2D, escrito 
#                  	en Python y utilizando las librerias Pygame y
#					PyOpenGL.
#
# Autor:         Franco Maciel
#
# Creado:        08/07/2014 (dd/mm/aa)
#
# Copyright:     (c) Franco Maciel 2014
#
# Licencia:      ¬¬
#-------------------------------------------------------------------------------


# Importamos todo para poder ser utilizados bajo un sólo módulo
from nucleo import Nucleo
from escena import Escena
from mapa_evento import MapaEvento
from capa import Capa
from objeto_base import ObjetoBase
from objeto_base import ObjetoImagen
from objeto_base import ObjetoImagenAvanzado
from objeto_animado import ObjetoAnimado
from camara import Camara
from shader import Shader
from framebuffer import Framebuffer
from vec2 import Vec2
