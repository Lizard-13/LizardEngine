#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 10/07/2014 (dd/mm/aa)

# Globales
from OpenGL.GL import *
from OpenGL.GL.shaders import *
from math import sin, cos, atan2, radians

# Locales
from vec2 import Vec2

class ObjetoBase():
    """Objeto básico con profundidad (orden de renderizado), control de
    actividad y una capa."""
    def __init__(self, z=0):
        """Inicializa el objeto.
        z = valor Z (orden de renderizado) del objeto"""
        print("Objeto Base creado")
        self.z = z
        self.activo = True
        self.capa = None
    def actualizar(self, tiempo):
        """Actualización en cada fotograma.
        tiempo = tiempo transcurrido desde el último fotograma"""
        if self.activo:
            self.accion_activa(tiempo)
        else:
            self.accion_pasiva(tiempo)
    def accion_activa(self, tiempo):
        """Funciones de alto consumo cuando el objeto entra en juego.
        tiempo = tiempo transcurrido desde el último fotograma"""
        pass
    def accion_pasiva(self, tiempo):
        """Funciones de bajo consumo para activar el objeto.
        tiempo = tiempo transcurrido desde el último fotograma"""
        pass
    def renderizar(self):
        """Renderizar el objeto."""
        pass
    def destruir(self):
        """Destruye referencias del objeto."""
        self.capa = None

    def __del__(self):
        print("Objeto Base destruido")


class ObjetoImagen(ObjetoBase):
    """Objeto de renderizado incompleto, para heredar y especializar.
    pos = posición (respecto al punto origen) del objeto
    z = valor Z (orden de renderizado) del objeto"""
    def __init__(self, pos=(0,0), z=0):
        ObjetoBase.__init__(self, z)
        self.pos = Vec2(pos)
        self.angulo = 0.0
        self.escala = Vec2([1.0,1.0])
        self.programa = None

    def renderizar(self, puntos, textura, tam, camara):
        """Renderiza el objeto, al heredar
        hay que definir puntos, textura por
        defecto y tamaño"""
        # Obtener los puntos
        rotor = puntos["rotor"]
        origen = puntos["origen"]
        # Guardar la matriz de cámara para los otros objetos
        glPushMatrix()
        # Transformaciones de la matriz del objeto
        glTranslatef(self.pos.x - origen.x + rotor.x,
                     self.pos.y - origen.y + rotor.y, 0.0)
        glRotatef(-self.angulo, 0.0, 0.0, 1.0)
        glTranslatef(-rotor.x, -rotor.y, 0.0)
        # Por defecto se activa GL_TEXTURE0 con la textura 0
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, textura)
        # Si se ha establecido un programa, usarlo y actualizarlo:
        if self.programa:
            glUseProgram(self.programa)
            self.actualizar_programa()
        # Dibujar el objeto en el framebuffer de la cámara
        camara.renderizar_cuad(0., 0.,
                               tam[0]*self.escala.x, tam[1]*self.escala.y)
        # Si se ha establecido un programa, cerrarlo:
        if self.programa:
            glUseProgram(0)
        # Finalizar el uso de las matrices del objeto
        glPopMatrix()

        # Renderizado de prueba (toma en cuenta las transformaciones del objeto)
        self.renderizado_de_prueba()

    def agregar_programa(self, programa):
        """Establecer un nuevo programa como programa del objeto."""
        self.programa = programa    #Establecer el programa
        glUseProgram(self.programa)    #Usar el programa
        self.iniciar_programa()        #Valores iniciales del programa
        glUseProgram(0)                #Cerrar el programa

    def iniciar_programa(self):
        """Debería ser usado para establecer
        valores iniciales no variables del
        programa, como algunas texturas"""
        pass            #Debe ser reescrito en la herencia

    def actualizar_programa(self):
        """Debería ser usado para establecer
        constantemente valores variables del
        programa, como el tiempo"""
        pass            #Debe ser reescrito en la herencia

    def mirar_a(self, punto):
        """Rota el objeto para apuntar
        hacia el punto dado"""
        punto_objeto = self.pos+self.puntos["rotor"]-self.puntos["origen"]
        self.angulo = -atan2(punto.y-punto_objeto.y, punto.x-punto_objeto.x)*180.0/3.141592

    def rotar_punto(self, punto, angulo):
        """Rota un punto utilizando
        trigonometría básica"""
        coseno = cos(radians(-angulo))
        seno = sin(radians(-angulo))
        return Vec2((coseno*punto.x-seno*punto.y, seno*punto.x+coseno*punto.y))

    def pos_abs_p(self, punto, puntos):
        """Retorna la posición absoluta
        del punto en el espacio"""
        return self.pos-puntos["origen"] + self.rotar_punto(punto-puntos["rotor"],self.angulo) + puntos["rotor"]
        #          posición absoluta                punto rotado respecto al rotor              devolvemos el rotor

    def renderizado_de_prueba(self, puntos):
        """Renderizado de puntos para verificar
        que las posiciones son correctas, al
        heredar hay que definir los puntos"""
        origen = self.pos_abs_p(puntos["origen"], puntos)
        centro = self.pos_abs_p(puntos["centro"], puntos)
        rotor = self.pos_abs_p(puntos["rotor"], puntos)
        #glLoadIdentity()
        glBegin(GL_POINTS)
        glColor3f(0.4,0.8,0.4)
        glVertex3f(rotor.entero()[0],rotor.entero()[1],0.0)
        glColor3f(0.4,0.4,0.8)
        glVertex3f(origen.entero()[0],origen.entero()[1],0.0)
        glColor3f(0.8,0.4,0.4)
        glVertex3f(centro.entero()[0],centro.entero()[1],0.0)
        glEnd()
        glColor3f(1.0,1.0,1.0)



class ObjetoImagenAvanzado(ObjetoImagen):
    """Objeto de renderizado básico
    sin animaciones, puede tener
    varias texturas para shaders"""
    def __init__(self, textura, pos=(0,0), z=0):
        ObjetoImagen.__init__(self, pos, z)
        self.texturas = [textura]

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texturas[0])
        self.tam = (glGetTexLevelParameterfv(GL_TEXTURE_2D, 0,  GL_TEXTURE_WIDTH),
                    glGetTexLevelParameterfv(GL_TEXTURE_2D, 0,  GL_TEXTURE_HEIGHT))

        self.puntos = {"origen": Vec2((0,0)),
                       "centro": Vec2(self.tam)*0.5,
                       "rotor" : Vec2(self.tam)*0.5}

    def renderizar(self, camara):
        """Renderiza el objeto"""
        puntos = self.puntos
        tam = self.tam
        textura = self.texturas[0]
        ObjetoImagen.renderizar(self, puntos, textura, tam, camara)
        #renderizado de prueba
        #self.renderizado_de_prueba()

    def renderizado_de_prueba(self):
        """Renderizado de puntos para verificar
        que las posiciones son correctas"""
        puntos = self.puntos
        ObjetoImagen.renderizado_de_prueba(self, puntos)
