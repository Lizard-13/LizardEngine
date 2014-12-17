#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 8/07/2014 (dd/mm/aa)

# Globales


class Capa():
    """La capa tiene la función de separar diferentes grupos de objetos para
    ser renderizados en un orden y con cámaras específicos."""
    def __init__(self, nombre, z=0):
        """Inicializa la capa.
        z = valor Z (orden de renderizado) de la capa"""
        print("Capa creada")
        self.nombre = nombre
        self.z = z
        self.visible = True
        self.escena = None
        self.objetos = []
        # Hay que agregar cámaras al iniciar
        self.camaras = []

    def actualizar(self, tiempo):
        """Actualiza las cámaras.
        tiempo = tiempo transcurrido desde el último fotograma"""
        for camara in self.camaras:
            camara.actualizar(tiempo)

    def renderizar(self):
        """Llama a renderizar a cada cámara, y a cada objeto por cámara."""
        # Sólo se renderiza si la capa es visible
        if self.visible:
            # Renderizar cada cámara
            for camara in self.camaras:
                # Activar framebuffers de cámara (si tiene)
                camara.iniciar_renderizado()
                # Renderizar cada objeto
                for objeto in self.objetos:
                    objeto.renderizar(camara)
                # Renderizar framebuffers a la pantalla
                camara.finalizar_renderizado()

    def agregar_camara(self, camara):
        """Agrega una cámara a la capa.
        camara = cámara a agregar"""
        self.camaras.append(camara)
        # Darle a la cámara información sobre la capa
        camara.capa = self
    
    def eliminar_camara(self, camara):
        """Elimina una cámara de la capa.
        camara = camara a eliminar"""
        camara.destruir()
        self.camaras.remove(camara)
    
    def ordenar_camaras(self):
        """Ordena las cámaras por su valor Z."""
        self.camaras.sort(key=lambda camara: camara.z)
    
    def agregar_objeto(self, objeto):
        """Agrega un nuevo objeto a la capa.
        objeto = objeto a agregar"""
        self.objetos.append(objeto)
        self.ordenar_objetos()
        # Se da al objeto información de su capa
        objeto.capa = self
    
    def eliminar_objeto(self, objeto):
        """Elimina un objeto de la capa, el objeto no es destruido.
        objeto = objeto a eliminar"""
        self.objetos.remove(objeto)
    
    def ordenar_objetos(self):
        """Ordena los objetos por su valor Z."""
        self.objetos.sort(key=lambda objeto: objeto.z)
    
    def destruir(self):
        # Eliminar referencias para que la escena pueda destruir la capa
        del self.escena
        # Eliminar las referencias de las cámaras
        for camara in self.camaras:
            camara.destruir()
        # Al no tener referencias, son eliminadas al ser olvidadas por la capa
        del self.camaras
        # Los objetos deben ser destruidos por la escena
        del self.objetos

    def __del__(self):
        print("Capa eliminada")
