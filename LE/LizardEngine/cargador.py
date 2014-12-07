#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 22/07/2014 (dd/mm/aa)


#Globales
import json
from OpenGL.GL import *
from copy import copy

#Locales
from vec2 import Vec2


class Cargador():
	def __init__(self):
		pass
	def cargar_escena(self, archivo, escena):
		archivo_abierto = open(archivo, "r")

		datos = json.load(archivo_abierto)

		for img in datos["Imagenes"]:
			escena.agregar_textura(img)

		for obj in datos["Objetos"]:
			modulo = __import__(obj["modulo"], globals={"__name__": __name__})
			objeto = getattr(modulo, obj["clase"])
			tipo = obj["tipo"]

			# Plantilla para crear las instancias
			objeto_base = None
			if obj["clase"] == "ObjetoAnimado":
				objeto_base = objeto()
				objeto_base.tipo = tipo
				for prop in obj["base"]:
					if prop == "anims":
						for anim in obj["base"]["anims"]:
							clase_animacion = getattr(modulo, "Animacion")
							animacion = clase_animacion()
							animacion.tpf = anim["tpf"]
							for ftgr in anim["ftgrs"]:
								clase_fotograma = getattr(modulo, "Fotograma")
								fotograma = clase_fotograma(escena.texturas[int(ftgr["imagen"])])
								for punto in ftgr["puntos"]:
									fotograma.puntos[punto] = Vec2(ftgr["puntos"][punto])
								animacion.agregar_ftgr(fotograma)
							objeto_base.agregar_anim(animacion)
				# Instancias
				for inst in obj["instancias"]:
					instancia = objeto()
					instancia.tipo = objeto_base.tipo
					trigger_once = True
					for a in objeto_base.anims:
						instancia.agregar_anim(copy(a))
						if trigger_once:
							instancia.anim_actual = instancia.anims[0]#[0, instancia.anims[0]]
							instancia.anims[0].ftgr_actual = 0
							trigger_once = False
					for prop in inst:
						if prop == "pos":
							instancia.pos = Vec2(inst[prop])
						elif prop == "puntos":
							for punto in inst[prop]:
								instancia.puntos[punto] = Vec2(inst[prop][punto])
						else:
							instancia.__dict__[prop] = inst[prop]
					escena.agregar_objeto(instancia)

			elif obj["clase"] == "ObjetoImagenAvanzado":
				for inst in obj["instancias"]:
					instancia = objeto(escena.texturas[inst["imagen"]])
					instancia.tipo = tipo
					for prop in inst:
						if prop == "pos":
							instancia.pos = Vec2(inst[prop])
						elif prop == "puntos":
							for punto in inst[prop]:
								instancia.puntos[punto] = Vec2(inst[prop][punto])
						else:
							instancia.__dict__[prop] = inst[prop]
					escena.agregar_objeto(instancia)

		archivo_abierto.close()
