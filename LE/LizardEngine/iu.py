#!/usr/bin/python
# -*- coding: utf-8 -*-
# creado: 23/07/2014 (dd/mm/aa)


# example base.py

import pygtk
pygtk.require('2.0')
import gtk

class Aplicacion():
	"""Ejemplo de aplicación con PyGTK, para familiarizar la librería."""
	def __init__(self):
		self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.ventana.connect("delete_event", self.eliminar_evento)	#Al hacer click en "cerrar ventana"
		self.ventana.connect("destroy", self.destruir)				#Al cerrar la ventana
		self.ventana.set_border_width(100)
		
		self.caja = gtk.HBox(False, 0)
		self.ventana.add(self.caja)
		
		self.boton1 = gtk.Button("Hola Mundo")
		self.boton1.connect("clicked", self.hola, "Boton 1")
		self.caja.pack_start(self.boton1, True, True, 0)
		
		self.boton2 = gtk.Button("Hola Mundo")
		self.boton2.connect("clicked", self.hola, "Boton 2")
		self.caja.pack_start(self.boton2, True, True, 0)
		
		def agregar_boton(n):
			for i in range(n):
				self.boton = gtk.Button("B%i"%(i+3))
				self.boton.connect("clicked", self.hola, "Boton %i"%(i+3))
				self.caja.pack_start(self.boton, True, False, 0)
				self.boton.show()
				
		agregar_boton(6)
		
		self.boton1.show()
		self.boton2.show()
		self.caja.show()
		self.ventana.show()
		
		
	def hola(self, widget, dato=None):
		print widget,dato, "Hola Mundo"
	def eliminar_evento(self, widget, evento, dato=None):
		print widget,evento,dato, "Eliminar"
		try:
			self.ventana_salir.destroy()
		except: pass
		self.ventana_salir = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.ventana_salir.set_border_width(10)
		self.boton_salir = gtk.Button("Salir?")
		self.boton_salir.connect_object("clicked", gtk.Window.destroy, self.ventana)
		self.ventana_salir.add(self.boton_salir)
		self.boton_salir.show()
		self.ventana_salir.show()
		return True										#Falso ==> destruir()
	def destruir(self, widget, dato=None):
		print widget,dato, "Destruir"
		gtk.main_quit()										#Cerrar todo

	def ejecutar(self):
		gtk.main()

print __name__
if __name__ == "__main__":
	aplicacion = Aplicacion()
	aplicacion.ejecutar()
