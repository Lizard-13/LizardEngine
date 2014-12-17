#===============================================================================
# Para Hacer:
#   ()=No, (*)=En proceso, (**)=Por buen camino, (***)=Finalizado por ahora
#   Generales:
# 	    (**) Reimplementar la renderizacion, a través de OpenGL
#              (faltan detalles como mejorar el objeto shader, FBO, e
#               implementar transformaciones correctas de la cámara y su
#               uso de dichos objetos gráficos)
############### Observando los impactos en el rendimiento de 1000 imágenes no
############### animadas, creo que es correcto replantear la idea cargar la
############### textura de cada objeto fotograma a fotograma, la solución más
############### factible sería ubicar los objetos en grupos de renderización,
############### en estos grupos, ordenarlos según su textura y posiblemente
############### shaders, y renderizar todo el grupo a la vez, también he de
############### tener en cuenta el uso de funciones actualizadas de OpenGL,
############### como los VAO y VBO.
#       (*)  Incluir ejemplos
#              (la arquitectura ya está terminada, mejorar objetos mientras se
#               implementan sus ejemplos correspondientes)
#       ()   Implementar física
#              (tal vez lo más díficil, utilizar PyBox2D)
# 	Ojetos Imagen:
# 		(**) Calcular la renderizacion, con diferentes cámaras y tamaños
#              (organizar mejor las transformaciones de la cámara - escala)
# 		(***)Usar shaders
#              (por ahora parecen estan contemplados la mayoría de métodos
#               de utilización básicos)
# 		(***)ObjetoAnimado y ObjetoImagenAvanzado herederos de la misma clase
#              (ahora es más fácil actualizar funciones comunes a ambos)
# 	Cámaras:
#       (***)Obligar posterior creación de cámaras para la escena
#              (ya es obligatorio crearlas)
# 		(*)  Posición y tamaño
#              (mejorar transformaciones, la posición a partir del centro
#               parece más intuitiva y el acercamiento sería hacia el centro)
# 		(*)  Zoom
#              (aparentemente fácil con Scalef() de OpenGL)
# 		(***)FBOs
#              (ya es obligatorio crearlos, la mayoría de métodos de uso básico
#               parecen estar contemplados)
# 	Caja de Recursos:
# 		()   Objeto separado de la escena
#              (no iniciado)
# 		(**) Implementar texturas
#              (cargar nuevas texturas es relativamente fácil)
# 		()   Implementar sonidos
#              (no iniciado, ¿PyOpenAL llevado a 2D o Pygame?)
#       ()   ¿Shaders y FBOs en la caja de recursos?
#              (Sólo shaders, ubicar fbos no tiene sentido ya que los fbos y
#               sus texturas son usados en particular por cada cámara.
#   Ideas para nuevos objetos:
#       ()   Objeto Mosaico
#              (posición de textura variable, podria heredar de ObjetoImagen,
#               ObjetoImagenAvanzado e inclusive de ObjetoAnimado)
#       ()   Objeto Texto
#              (sencillo para crear y renderizar textos)
#       ()   Objeto Sonido (espacial)
#              (proiedades de posición, volumen, fácil manejo de sonidos)
#       ()   Objeto Malla3D
#              (con OpenGL sería relativamente fácil renderizar mallas 3D,
#               podría incluirse un esqueleto para animaciones, puede que se
#               requiera un nuevo vector Vec3)
#===============================================================================
