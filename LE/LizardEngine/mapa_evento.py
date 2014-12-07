#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 5/08/2014 (dd/mm/aa)

#Globales
import pygame
from pygame.locals import *


# Hay que reorganizar toda la clase, la forma en la que funciona no ofrece
# ninguna mejora de rendimiento, itera sobre todos los eventos de Pygame,
# cuando sólo tiene que tener en cuenta los eventos definidos.

class MapaEvento():
    def __init__(self):
        self.entrada_teclado = {}
        self.entrada_raton = {1:[0,0], 2:[0,0], 3:[0,0], 4:[0,0], 5:[0,0]}   #Indices definidos por pygame: 1=izq,2=cen,3=der,4=r_ar,5=r_ab
        self.entrada_otros = {} #{tipo:valor}

    def actualizar_i(self):
        #Eventos del teclado
        eventos = pygame.event.get()

        for eve in eventos:
            if eve.type == pygame.KEYDOWN:              #Si la tecla del mapa se presiona
                if eve.key in self.entrada_teclado:     #Si la tecla esta en nuestro mapa de teclas
                    self.entrada_teclado[eve.key][0]=1  #Presionada
                    self.entrada_teclado[eve.key][1]=1  #Por primera vez
            elif eve.type == pygame.KEYUP:                #Si la tecla del mapa se suelta
                if eve.key in self.entrada_teclado:     #Si la tecla esta en nuestro mapa de teclas
                    self.entrada_teclado[eve.key][0]=0  #Presionada
                    self.entrada_teclado[eve.key][1]=1  #Por primera vez
            elif eve.type == pygame.MOUSEBUTTONDOWN:
                if eve.button in self.entrada_raton:       #Si el boton del raton se presiona
                    self.entrada_raton[eve.button][0]=1    #Presionada
                    self.entrada_raton[eve.button][1]=1    #Por primera vez
            elif eve.type == pygame.MOUSEBUTTONUP:
                if eve.button in self.entrada_raton:       #Si el boton del raton se suelta
                    self.entrada_raton[eve.button][0]=0    #Presionada
                    self.entrada_raton[eve.button][1]=1    #Por primera vez
            elif eve.type in self.entrada_otros:
                self.entrada_otros[eve.type]=1
                    
    #
    #Eventos en el nucleo...
    #
    def actualizar_f(self):
        for t,v in self.entrada_teclado.items():  #Al finalizar ya no se presiona por primera vez
            v[1] = 0
        for b,v in self.entrada_raton.items():
            v[1] = 0
        for t,v in self.entrada_otros.items():
            v = 0

    def definir_teclas(self, *teclas): #[nombre_tecla, tecla]
        for tecla in teclas:
            self.entrada_teclado[tecla] = [0,0]  #{tecla: [presionada, primera_vez]}

    def definir_otro(self, *tipos):
        for tipo in tipos:
            self.entrada_otros[tipo] = 0
