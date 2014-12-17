#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 8/07/2014 (dd/mm/aa)


#########################################################################
### Las listas iteran más rápido, los diccionarios acceden más rápido ###
#########################################################################
#Globales
import pygame
from pygame.locals import *
from OpenGL.GL import *

#Locales
from capa import Capa


class Escena():
    """La escena contiene los objetos, las capas y texturas, ordena la
    actualización de los objetos y capas. Sólo hay una escena activa
    a la vez."""
    def __init__(self, nombre, color=(0.1, 0.1, 0.1, 0.0),
                       tam=(800, 600), pant_compl=False):
        """Inicializa la escena.
        nombre = nombre de la escena (título de la ventana por defecto)
        color = color de fondo (de limpiado) de la escena
        tam = tamaño de la ventana de la escena
        pant_compl = ejecutar en pantalla completa"""
        print("Escena creada")
        self.nombre = nombre
        self.color = color
        self.tam = tam
        self.pant_compl = pant_compl
        self.nucleo = None
        # Capas por nombre
        self.capas = {}
        # Capas por orden Z
        self.capas_ord = []
        # Una capa por defecto (capa base)
        self.agregar_capa(Capa("Base"), False)
        # Grupos por nombre, instancias en sets
        self.objetos = {}
        # Recursos (posiblemente el sistema se modificará pronto)
        self.texturas = []
        self.eventos = None

    def actualizar(self, tiempo):
        """Actualiza la lógica de la escena y llama a actualizar a todos los
        objetos y las capas.
        tiempo = tiempo transcurrido desde el último fotograma"""
        # Ejecutar la lógica de escena
        self.logica(tiempo)
        # Actualizar objetos
        for grupo in self.objetos.values():
            for objeto in grupo:
                objeto.actualizar(tiempo)
        # Actualizar capas
        for capa in self.capas_ord:
            capa.actualizar(tiempo)

    def logica_ini(self):
        """Lógica a ejecutar una sola vez al iniciar la escena."""
        pass
            
    def logica(self, tiempo):
        """Lógica a ejecutar continuamente.
        tiempo = tiempo transcurrido desde el último fotograma"""
        pass

    def renderizar(self):
        """Llama a renderizar cada capa."""
        for capa in self.capas_ord:
            capa.renderizar() if capa.visible else None

    def agregar_capa(self, capa, ordenar=True):
        """Agrega una capa y puede ordenarlas por su valor Z.
        capa = capa a agregar
        ordenar = ordenar las capas (False = No ordenar)"""
        # Se agrega la capa a ambas listas
        self.capas[capa.nombre] = capa
        self.capas_ord.append(capa)
        # Dar a la capa información de la escena
        capa.escena = self
        # Ordenar las capas si corresponde
        if ordenar:
            self.ordenar_capas()
    
    def eliminar_capa(self, capa):
        """Remueve una capa de la escena.
        capa = capa a eliminar"""
        capa.destruir()
        del self.capas[capa.nombre]

    def ordenar_capas(self):
        """Ordena las capas por su valor Z."""
        self.capas_ord.sort(key=lambda capa: capa.z)
    
    def a_capa_superior(self, nombre):
        """Mueve la capa sobre todas las demás.
        nombre = nombre de la capa a mover"""
        # El mayor valor Z entre todas las capas (excepto ésta) +1
        capa = self.capas[nombre]
        capa.z = max(cp.z for cp in self.capas_ord if cp != capa) + 1
        # Luego de cambiar su posición, ordenarlas
        self.ordenar_capas()

    def a_capa_inferior(self, capa):
        """Mueve la capa debajo de todas las demás.
        nombre = nombre de la capa a mover"""
        # El menor valor Z entre todas las capas (excepto ésta) -1
        capa.z = min(cp.z for cp in self.capas_ord if cp != capa)  - 1
        # Luego de cambiar su posición, ordenarlas
        self.ordenar_capas()
        
    def agregar_objeto(self, objeto, capa=None):
        """Agrega un objeto a una capa.
        objeto = objeto a agregar a la capa
        capa = capa a la cual agregar"""
        # Agregar el objeto en su lista de grupo
        nombre = objeto.nombre
        if nombre in self.objetos:
            self.objetos[nombre].add((objeto))
        else:
            self.objetos[nombre] = set([objeto])
        # Si no se explicita una capa, se usa la capa base
        if not capa:
            capa = self.capas["Base"]
        # Se agrega el objeto a la capa
        capa.agregar_objeto(objeto)
    
    def eliminar_objeto(self, objeto):
        """Elimina un objeto de la escena.
    	objeto = objeto a eliminar"""
        # Se destruyen las referencias del objeto
        objeto.destruir()
        # Se elimina el objeto de su grupo en la escena
        self.objetos[objeto.nombre].remove(objeto)
        
    def ordenar_objetos(self, capa=None):
        """Llama a cada capa a ordenar los objetos
        por su valor Z.
        capa = capa a restringir el orden"""
        # Si no se da una capa, se ordenan los objetos de todas las capas
        if not capa:
            for capa in self.capas_ord:
                capa.ordenar_objetos()
        else:
            capa.ordenar_objetos()
    
    def mover_a_capa(self, objeto, capa):
        """Mueve un objeto desde su capa original a otra.
        objeto = objeto a mover
        capa = nueva capa del objeto"""
        # Se elimina el objeto de su antigua capa
        objeto.capa.eliminar_objeto(objeto)
        # Se agrega a la nueva
        capa.agregar_objeto(objeto)

    def agregar_textura(self, img):
        """Agrega una textura la lista de la escena a partir de una imagen.
        img = archivo imagen a agregar como textura"""
        # Transformar en imagen legible para OpenGL
        imagen = pygame.image.load(img)
        textura_info = pygame.image.tostring(imagen, "RGBA", 1)
        # Obtener el tamaño
        ancho, alto = imagen.get_size()
        # Crear la textura
        textura = glGenTextures(1)
        # Usarla
        glBindTexture(GL_TEXTURE_2D, textura)
        # Establecer los parámetros (incluyendo la imagen misma)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ancho, alto, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, textura_info)
        # Agregar la textura
        self.texturas.append(textura)
        

    def cargar_escena(self, archivo):
        """Carga objetos y recursos de un archivo a través del cargador de
        recursos del núcleo.
        archivo = archivo a cargar"""
        try:
            self.nucleo.cargador.cargar_escena(archivo, self)
        except IOError:
            raise Exception("No se encontró {archivo}".format(archivo=archivo))
           
    def destruir(self):
        # Limpiar las texturas
        glDeleteTextures(self.texturas)
        # Elimina referencias para poder eliminarlos
        del self.nucleo
        del self.eventos
        # Destruir objetos para eliminar sus referencias
        for grupo in self.objetos.values():
            for objeto in grupo:
                objeto.destruir()
        # Destruir capas para eliminar sus referencias
        for capa in self.capas_ord:
            capa.destruir()
        # Al no tener referncias, son eliminados al ser olvidados por la escena
        del self.objetos
        del self.capas
        del self.capas_ord

    def __del__(self):
        print("Escena eliminada")
