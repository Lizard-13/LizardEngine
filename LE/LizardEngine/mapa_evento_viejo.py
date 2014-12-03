import pygame
#from pygame.locals import *


class MapaEvento():
    def __init__(self):
        self.entrada_teclado = {}
        self.entrada_raton = {'izq':[],'cen':[],'der':[]}
        self.entrada_otros = {}

    def actualizar_i(self):
        #Eventos del teclado
        teclas = pygame.key.get_pressed()
        for t,v in self.entrada_teclado.items(): #tecla,valor
            if teclas[v[0]] and v[1] == 0:  #Si la tecla del mapa esta presionada y es la primera vez
                v[1]=1                          #Presionada
                v[2]=1                          #Por primera vez
            elif not teclas[v[0]] and v[1] == 1:    #Si la tecla del mapa no esta presionada y es la primera vez
                v[1]=0                                  #No presionada
                v[2]=1                                  #Por primera vez
        #print self.entrada_teclado
        #Eventos del raton
        botones = pygame.mouse.get_pressed()
        #evento = pygame.event.Event(MOUSEROLL)
        print pygame.event.poll(pygame.MOUSEBUTTONDOWN)

    #
    #Eventos en el nucleo...
    #
    def actualizar_f(self):
        for t,v in self.entrada_teclado.items():  #Al finalizar ya no se presiona por primera vez
            v[2] = 0

    def definir_teclas(self, *teclas): #[nombre_tecla, tecla]
        for tecla in teclas:
            self.entrada_teclado[str(tecla)] = [tecla, 0,0]  #{tecla: [tecla, presionada, primera_vez]}