#!/usr/bin/env python

#Script en Python para Gimp, el mismo permite generar, borrar,renombrar, duplicar y EDITAR pinceles generados a partir de imagenes o de otro pincel.

#Copyright (c) (2008) Marcelo "Tanda" Cervi&o.
#Argentina. 
#  http://lodetanda.blogspot.com -- lodetanda @ gmail.com

# Este programa es un software de libre distribucion, que puede ser copiado y distribuido bajo los terminos de la Licencia Publica General GNU, de acuerdo con la publicada por la Free Software Foundation, version 3 de la licencia o (a criterio del autor) cualquier version posterior.
#Este programa se distribuye con la expectativa de ser util a sus usuarios, pero NO TIENE GARANTIA ALGUNA, EXPLICITAS O IMPLICITAS, COMERCIALES O DE ATENCION A UNA DETERMINADA FINALIDAD Consulta la Licencia Publica General #GNU para mayores detalles.

#Debe haber una copia de la Licencia Publica General GNU junto con este software. Si no escriba a Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

#Tanda-GIMP-Python-Fu-EditBrushes-V2.1 ----03/2008----.
#Alojado en github ----09/2016----.

from gimpfu import *
import os

##################01-Editar pincel.

def editar(image, drawable, porcentaje, aspectox, aspectoy, angulo, esp, flip,):

		
		ruta_pinceles = pdb.gimp_gimprc_query("brush-path-writable")
		brush = pdb.gimp_context_get_brush()
		archivos = os.listdir(ruta_pinceles)

		imagen_origen = ruta_pinceles+os.sep+brush
	

		if brush+'(brush)'+'.gbr' and brush in archivos:
		
			img = pdb.gimp_file_load(imagen_origen, imagen_origen)
		
			ancho = ((((img.width * porcentaje) / 100) * aspectox) / 100)+1
			alto = ((((img.height * porcentaje) / 100) * aspectoy) / 100)+1

			gris = pdb.gimp_drawable_is_gray(img.layers[0])

			pdb.gimp_image_scale(img, ancho, alto)
		
			pdb.gimp_drawable_transform_rotate_default(img.layers[0], (((angulo+1)*3.141592)/180), True, (img.height/2),(img.height/2), True, True)
		
			fondo_original = gimp.get_background()
		
			pdb.gimp_context_set_background((255,255,255))
		
			if gris == True:
				pdb.gimp_image_flatten(img)
			
			if flip == 0 or flip == 1:
				pdb.gimp_image_flip(img, flip)
			
			guardar_pincel = ruta_pinceles+os.sep+img.name+'(brush)'+'.gbr'

			pdb.file_gbr_save(img, img.layers[0], guardar_pincel, guardar_pincel, esp, img.name)
			pdb.gimp_brushes_refresh(img)
			pdb.gimp_context_set_background(fondo_original)
			pdb.gimp_image_delete(img)
		else:
			pdb.gimp_message("El pincel //"+str(brush)+"//  no es editable")

if __name__ == '__main__':

	register(
		"Editar_Pincel",
		"Modifica las propiedades de cualquier pincel creado con los scripts -Pincel activo a pincel editable-, -Imagen activa a pincel editable- o -Imagen en disco a pincel editable-, sus nombres comienzan con (E).",
		"Editar Pincel",
		"Tanda",
		"Tanda",
		"2008",	
		"<Image>/Pinceles/01-Editar pinceles/01-Editar pincel",
		"RGB*, GRAY*",
		[
			(PF_SPINNER, "porcentaje", "Diametro %", 20, (1, 500, 1)),
			(PF_SPINNER, "aspectox", "proporcionX %", 100, (1, 100, 1)),
			(PF_SPINNER, "aspectoy", "proporcionY %", 100, (1, 100, 1)),
			(PF_SPINNER, "angulo", "Angulo", 0, (-360, 360, 1)),
			(PF_SPINNER, "esp", "Espaciado", 15, (1, 5000, 1)),
			(PF_RADIO, "flip", "Espejado", 2, (("Horizontal", 0), ("Vertical", 1), ("Ninguno", 2))),
		],
		[],
		editar)

##################02-Ver o editar imagen origen.

def origen(image, drawable):

		
		ruta_pinceles = pdb.gimp_gimprc_query("brush-path-writable")
		brush = pdb.gimp_context_get_brush()
		archivos = os.listdir(ruta_pinceles)
		imagen_origen = ruta_pinceles+os.sep+brush

		if brush+'(brush)'+'.gbr' and brush in archivos:

				img = pdb.gimp_file_load(imagen_origen, imagen_origen)
				pdb.gimp_display_new (img)
				pdb.gimp_message("Se acaba de abrir la imagen origen perteneciente al pincel //"+str(brush)+"//, una vez que haya hecho los cambios guardarlos con -ctrl+S- y la proxima vez que edite este pincel se actualizaran. Si en la edicion se aumento la resolucion, para que se actualice en el nombre del pincel se tiene que cambiar el nombre del mismo con el script -Renombrar pincel editable-.")
		else:
			pdb.gimp_message("El pincel //"+str(brush)+"//  no posee imagen origen porque NO es editable.")
			
		
if __name__ == '__main__':


	register(
		"ver_o_editar_imagen_origen",
		"ver o editar la imagen origen perteneciente al pincel activo.    Tanda.",
		"ver_o_editar_imagen_origen",
		"Tanda",
		"Tanda",
		"2008",	
		"<Image>/Pinceles/01-Editar pinceles/02-Ver o editar imagen origen",
		"RGB*, GRAY*",
		[],
		[],
		origen)

################01- Pincel activo a pincel editable.

def actual(image, drawable,  nombre, guardarcomo, porcentaje, esp, colorbrush, fixrotacion):
		
	ruta_pinceles = pdb.gimp_gimprc_query("brush-path-writable")
	fondo_original = gimp.get_background()
	frente_original = gimp.get_foreground()
		
	brush = pdb.gimp_context_get_brush()
	brushdimen = pdb.gimp_brush_get_info(brush) 
	w,h,mbpp,cbpp = brushdimen
	st = [w/2,h/2]
	img = pdb.gimp_image_new(w, h, colorbrush)
	
	capa = pdb.gimp_layer_new(img, w, h, colorbrush+1, "capa", 100, 0)
	pdb.gimp_image_add_layer(img, capa, 0)
	if guardarcomo == ".jpg" and colorbrush == 0:
		pdb.gimp_edit_fill(capa, BACKGROUND_FILL)
	
	pdb.gimp_context_set_background((255,255,255))
	pdb.gimp_context_set_foreground((0,0,0))
	
	if colorbrush == 1:
		pdb.gimp_edit_fill(capa, BACKGROUND_FILL)
	
	pdb.gimp_context_set_background((255,255,255))
	pdb.gimp_context_set_foreground((0,0,0))
	pdb.gimp_paintbrush_default(capa, 2, st)

	reso = '(max'+str(img.width)+')'
	archivos = os.listdir(ruta_pinceles)
	nombre_pincel = '(E)'+nombre+reso+guardarcomo
	
	while nombre_pincel in archivos:

		nombre_pincel = '(E)'+nombre_pincel

	if fixrotacion == 1:
		rotado = (img.width**2 + img.height**2)**0.5
		despx = (rotado - img.width) / 2
		despy = (rotado - img.height) / 2
		pdb.gimp_image_resize(img, rotado, rotado, despx, despy)
		pdb.gimp_layer_resize_to_image_size(img.layers[0])


	guardar_imagen = ruta_pinceles+os.sep+nombre_pincel
	guardar_pincel = guardar_imagen+'(brush)'+'.gbr'
	
	ancho = ((img.width * porcentaje) / 100) 
	alto = ((img.height * porcentaje) / 100)

	pdb.gimp_file_save(img, img.layers[0], guardar_imagen, guardar_imagen)

	pdb.gimp_image_scale(img, ancho, alto)
	
	if colorbrush == 1:
		pdb.gimp_image_flatten(img)
	
	pdb.file_gbr_save(img,img.layers[0], guardar_pincel, guardar_pincel, esp, nombre_pincel)
	pdb.gimp_brushes_refresh(img)
	pdb.gimp_context_set_brush(nombre_pincel)
	pdb.gimp_image_delete(img)
	pdb.gimp_context_set_background(fondo_original)
	pdb.gimp_context_set_foreground(frente_original)
	pdb.gimp_message("Se ha creado un nuevo pincel editable llamado     "+str(nombre_pincel))

if __name__ == '__main__':

	register(
		"pinceles_a_pinceles_editables",
		"Crea un pincel a partir del activo, el mismo podra ser editado luego con el script -Editar Pincel-.",
		"pinceles_a_pinceles_editables",
		"Tanda",
		"Tanda",
		"2008",		
		"<Image>/Pinceles/02-Crear pinceles editables/01- Pincel activo a pincel editable",
		"RGB*, GRAY*",
		[
			(PF_STRING, "nombre", "Nombre", ""),
			(PF_RADIO, "guardarcomo", "Guardar imagen origen como", ".png", ((".png", ".png"), (".jpg", ".jpg"))),
			(PF_SPINNER, "porcentaje", "Diametro %", 100, (1, 500, 1)),
			(PF_SPINNER, "esp", "Espaciado", 15, (1, 5000, 1)),
			(PF_RADIO, "colorbrush", "Pintar con:", 1, (("color de la imagen", 0), ("colores a eleccion", 1))),
			(PF_RADIO, "fixrotacion", "Scale for fix rotate", 0, (("no", 0), ("si", 1))),
		],
		[],
		actual)

##############02-Imagen activa a pincel editable.

def crear_img_sel(image, drawable, nombre, guardarcomo, porcentaje, angulo, esp, colorbrush, fixrotacion):
	
	fondo_original = gimp.get_background()	
	ruta_pinceles = pdb.gimp_gimprc_query("brush-path-writable")
	img = pdb.gimp_image_duplicate(image)
	reso = '(max'+str(img.width)+')'
	archivos = os.listdir(ruta_pinceles)
	nombre_pincel = '(E)'+nombre+reso+guardarcomo

	while nombre_pincel in archivos:

		nombre_pincel = '(E)'+nombre_pincel
	
	if fixrotacion == 1:
		rotado = (img.width**2 + img.height**2)**0.5
		despx = (rotado - img.width) / 2
		despy = (rotado - img.height) / 2
		pdb.gimp_image_resize(img, rotado, rotado, despx, despy)

	ancho = ((img.width * porcentaje) / 100) 
	alto = ((img.height * porcentaje) / 100)
	rgb = pdb.gimp_drawable_is_rgb(img.layers[0])
	gris = pdb.gimp_drawable_is_gray(img.layers[0])

	if rgb == True  and colorbrush == 3:
		pdb.gimp_image_convert_grayscale(img)

	if gris == True  and colorbrush == 2:
		pdb.gimp_image_convert_rgb(img)
	
	if guardarcomo == ".jpg" and colorbrush == 2:
		pdb.gimp_image_flatten(img)
	if guardarcomo == ".png" and colorbrush == 2:
		pdb.gimp_layer_resize_to_image_size(img.layers[0])

	if colorbrush == 3:
		pdb.gimp_context_set_background((255,255,255))
		pdb.gimp_image_flatten(img)
		pdb.gimp_context_set_background(fondo_original)
	
	guardar_imagen = ruta_pinceles+os.sep+nombre_pincel	
	
	pdb.gimp_file_save(img, img.layers[0], guardar_imagen, guardar_imagen)

	pdb.gimp_image_scale(img, ancho, alto)
	pdb.gimp_drawable_transform_rotate_default(img.layers[0], (((angulo+1)*3.141592)/180), True, (img.height/2), (img.height/2), True, True)

	guardar_pincel = guardar_imagen+'(brush)'+'.gbr'

	if colorbrush == 3:
		pdb.gimp_context_set_background((255,255,255))
		pdb.gimp_image_flatten(img)
		pdb.gimp_context_set_background(fondo_original)
		
	pdb.file_gbr_save(img, img.layers[0], guardar_pincel, guardar_pincel, esp, nombre_pincel)
	pdb.gimp_brushes_refresh(img)
	pdb.gimp_context_set_brush(nombre_pincel)
	pdb.gimp_image_delete(img)
	pdb.gimp_message("Se ha creado un nuevo pincel editable llamado     "+str(nombre_pincel))
	
if __name__ == '__main__':

	register(
		"imagen_activa_a_pincel",
		"Crea un pincel a partir de la imagen activa, el mismo podra ser editado luego con el script -Editar Pincel-.",
		"imagen activa a pincel",
		"Tanda",
		"Tanda",
		"2008",		
		"<Image>/Pinceles/02-Crear pinceles editables/02-Imagen activa a pincel editable",
		"RGB*, GRAY*",
		[
			
			(PF_STRING, "nombre", "Nombre", ""),
			(PF_RADIO, "guardarcomo", "Guardar imagen origen como", ".png", ((".png", ".png"), (".jpg", ".jpg"))),
			(PF_SPINNER, "porcentaje", "Diametro %", 20, (1, 500, 1)),
			(PF_SPINNER, "angulo", "Angulo", 0, (-360, 360, 1)),
			(PF_SPINNER, "esp", "Espaciado", 15, (1, 5000, 1)),
			(PF_RADIO, "colorbrush", "Pintar con:", 3, (("color de la imagen", 2), ("colores a eleccion", 3))),
			(PF_RADIO, "fixrotacion", "Escalar para asegurar el rotado", 0, (("no", 0), ("si", 1))),
		],
		[],
		crear_img_sel)

###################03-Imagen en disco a pincel editable.

def crear_de_ruta(image, drawable, ruta, guardarcomo, nombre, porcentaje, angulo, esp, colorbrush, fixrotacion):

	fondo_original = gimp.get_background()	
	ruta_pinceles = pdb.gimp_gimprc_query("brush-path-writable")
	img = pdb.gimp_file_load(ruta,ruta)
	reso = '(max'+str(img.width)+')'
	archivos = os.listdir(ruta_pinceles)
	nombre_pincel = '(E)'+nombre+reso+guardarcomo


	while nombre_pincel in archivos:

		nombre_pincel = '(E)'+nombre_pincel

	if fixrotacion == 1:
		rotado = (img.width**2 + img.height**2)**0.5
		despx = (rotado - img.width) / 2
		despy = (rotado - img.height) / 2
		pdb.gimp_image_resize(img, rotado, rotado, despx, despy)
		pdb.gimp_layer_resize_to_image_size(img.layers[0])

	ancho = ((img.width * porcentaje) / 100) 
	alto = ((img.height * porcentaje) / 100)		
	rgb = pdb.gimp_drawable_is_rgb(img.layers[0])
	index = pdb.gimp_drawable_is_indexed(img.layers[0])
	gris = pdb.gimp_drawable_is_gray(img.layers[0])

	if (rgb == True or index == True) and colorbrush == 1:
		pdb.gimp_context_set_background((255,255,255))
		pdb.gimp_image_convert_grayscale(img)
		pdb.gimp_image_flatten(img)
		pdb.gimp_context_set_background(fondo_original)

	if (index == True or gris == True) and colorbrush == 0:
		pdb.gimp_image_convert_rgb(img)

	if guardarcomo == ".jpg" and colorbrush == 0:
		pdb.gimp_image_flatten(img)

	guardar_imagen = ruta_pinceles+os.sep+nombre_pincel
	guardar_pincel = guardar_imagen+'(brush)'+'.gbr'	

	pdb.gimp_file_save(img, img.layers[0], guardar_imagen, guardar_imagen)
	
	pdb.gimp_image_scale(img, ancho, alto)
	pdb.gimp_drawable_transform_rotate_default(img.layers[0], (((angulo+1)*3.141592)/180), True, (img.height/2), (img.height/2), True, True)

	if colorbrush == 1:
		pdb.gimp_context_set_background((255,255,255))
		pdb.gimp_image_flatten(img)
		pdb.gimp_context_set_background(fondo_original)
		
	pdb.file_gbr_save(img,img.layers[0], guardar_pincel, guardar_pincel, esp, nombre_pincel)
	pdb.gimp_brushes_refresh(img)
	pdb.gimp_context_set_brush(nombre_pincel)
	pdb.gimp_image_delete(img)
	pdb.gimp_message("Se ha creado un nuevo pincel editable llamado     "+str(nombre_pincel))

	
if __name__ == '__main__':

	register(
		"Imagen_en_disco_a_pincel",
		"Crea un pincel a partir de una imagen en el disco, el mismo podra ser editado luego con el script -Editar pincel-.",
		"Imagen en disco a pincel",
		"Tanda",
		"Tanda",
		"2008",		
		"<Image>/Pinceles/02-Crear pinceles editables/03-Imagen en disco a pincel editable",
		"RGB*, GRAY*",
		[
			(PF_FILE, "ruta", "imagen", ""),
			(PF_RADIO, "guardarcomo", "Guardar imagen origen como", ".png", ((".png", ".png"), (".jpg", ".jpg"))),
			(PF_STRING, "nombre", "Nombre", ""),
			(PF_SPINNER, "porcentaje", "Diametro %", 20, (1, 500, 1)),
			(PF_SPINNER, "angulo", "Angulo", 0, (-360, 360, 1)),
			(PF_SPINNER, "esp", "Espaciado", 15, (1, 5000, 1)),
			(PF_RADIO, "colorbrush", "Pintar con:", 1, (("color de la imagen", 0), ("colores a eleccion", 1))),
			(PF_RADIO, "fixrotacion", "Scale for fix rotate", 0, (("no", 0), ("si", 1))),
		],
		[],
		crear_de_ruta)
	
###############03-Duplicar pincel editable.

def duplicar(image, drawable, duplicar):

	fondo_original = gimp.get_background()
	pdb.gimp_context_set_background((255,255,255))	
	ruta_pinceles = pdb.gimp_gimprc_query("brush-path-writable")
	archivos = os.listdir(ruta_pinceles)
	brush = pdb.gimp_context_get_brush()
	brushdimen = pdb.gimp_brush_get_info(brush) 
	w,h,mbpp,cbpp = brushdimen
	esp = pdb.gimp_brush_get_spacing(brush)
	archivos = os.listdir(ruta_pinceles)
	
	if brush+'(brush)'+'.gbr' and brush in archivos:
		img = pdb.gimp_file_load(ruta_pinceles+os.sep+brush, ruta_pinceles+os.sep+brush)
		
		while brush in archivos:

			brush = str("(E)(copia)")+brush	
	
		if duplicar == 1:
			pdb.gimp_file_save(img, img.layers[0], ruta_pinceles+os.sep+brush, ruta_pinceles+os.sep+brush)
			pdb.gimp_image_scale(img, w, h)
			pdb.gimp_drawable_transform_rotate_default(img.layers[0], (0.023008889), True, (img.height/2),(img.height/2), True, True)
			pdb.gimp_image_flatten(img)
			pdb.file_gbr_save(img,img.layers[0], ruta_pinceles+os.sep+brush+'(brush)'+'.gbr', ruta_pinceles+os.sep+brush+'(brush)'+'.gbr', esp, brush)
			pdb.gimp_brushes_refresh(img)
			pdb.gimp_context_set_brush(brush)
			pdb.gimp_message("se a creado un nuevo pincel llamado   "+str(brush))
		else:
			pdb.gimp_message("El pincel NO fue duplicado.")
			pdb.gimp_context_set_background(fondo_original)
			pdb.gimp_image_delete(img)

	else:
		pdb.gimp_message("El pincel //"+str(brush)+"//  no es editable.")
	
if __name__ == '__main__':

	register(
		"Duplicar_Pincel",
		"Duplica el pincel activo y su imagen origen (solo para los pinceles creados con los scripts -Pincel activo a pincel editable-, -Imagen activa a pincel editable- o -Imagen en disco a pincel editable-, sus nombres comienzan con (E)).",
		"Duplicar Pincel",
		"tanda",
		"tanda",
		"2008",	
		"<Image>/Pinceles/01-Editar pinceles/03-Duplicar pincel editable",
		"RGB*, GRAY*",
		[
			(PF_RADIO, "duplicar", "Duplicar", 0, (("No", 0), ("Si", 1))),

		],
		[],
		duplicar)

###############04-Renombrar pincel editable.

def renombrar(image, drawable, renombre):

		fondo_original = gimp.get_background()
		pdb.gimp_context_set_background((255,255,255))
		ruta_pinceles = pdb.gimp_gimprc_query("brush-path-writable")
		archivos = os.listdir(ruta_pinceles)
		brush = viejobrush = pdb.gimp_context_get_brush()
		brushdimen = pdb.gimp_brush_get_info(brush) 
		w,h,mbpp,cbpp = brushdimen
		esp = pdb.gimp_brush_get_spacing(brush)
		guardar_imagen = ruta_pinceles+os.sep+brush
		extension = os.path.splitext (guardar_imagen)[1]
	
		if brush+'(brush)'+'.gbr' and brush in archivos:
			
			img = pdb.gimp_file_load(guardar_imagen, guardar_imagen)
		
			reso = '(max'+str(img.width)+')'
			ren =  ruta_pinceles+os.sep+'(E)'+renombre+reso+extension
			ren_pincel = ruta_pinceles+os.sep+'(E)'+renombre+reso+extension+'(brush)'+'.gbr'
			nombre_pincel = '(E)'+renombre+reso+extension

			

			while nombre_pincel in archivos:
				
				nombre_pincel = '(E)'+nombre_pincel
				
				ren = ruta_pinceles+os.sep+nombre_pincel
				ren_pincel = ruta_pinceles+os.sep+nombre_pincel+'(brush)'+'.gbr'

		
			pdb.gimp_image_scale(img, w, h)
			pdb.gimp_drawable_transform_rotate_default(img.layers[0], (0.023008889), True, (img.height/2),(img.height/2), True, True)
			pdb.gimp_image_flatten(img)
			pdb.file_gbr_save(img,	img.layers[0], ren_pincel, ren_pincel, esp, nombre_pincel)	
			pdb.gimp_brushes_refresh(img)
			os.rename(guardar_imagen, ren)
			pdb.gimp_context_set_brush(nombre_pincel)
			pdb.gimp_brush_delete(viejobrush)
			pdb.gimp_message("Su pincel ahora se llama   "+str(nombre_pincel))
			pdb.gimp_context_set_background(fondo_original)
			pdb.gimp_image_delete(img)
		else:
			pdb.gimp_message("El pincel //"+str(brush)+"//  no es editable.")

if __name__ == '__main__':

	register(
		"Renombrar_Pincel_editable",
		"Renombra el pincel activo y su imagen origen (solo para los pinceles creados con los scripts -Pincel activo a pincel editable-, -Imagen activa a pincel editable- o -Imagen en disco a pincel editable-, sus nombres comienzan con (E)).",
		"Renombrar Pincel editable",
		"Tanda",
		"Tanda",
		"2008",	
		"<Image>/Pinceles/01-Editar pinceles/04-Renombrar pincel editable",
		"RGB*, GRAY*",
		[
			(PF_STRING, "renombre", "Nombre nuevo", ""),

		],
		[],
		renombrar)

###############05-Borrar pincel editable.

def borrar(image, drawable, borrado):

		
		ruta_pinceles = pdb.gimp_gimprc_query("brush-path-writable")
		archivos = os.listdir(ruta_pinceles)
		brush = pdb.gimp_context_get_brush()
		guardar_imagen = ruta_pinceles+os.sep+brush
		
		if brush+'(brush)'+'.gbr' and brush in archivos:	
			
			img = pdb.gimp_file_load(guardar_imagen, guardar_imagen)
	
			if borrado == 1:
				os.remove(guardar_imagen)

				pdb.gimp_brush_delete(brush)
				pdb.gimp_brushes_refresh(img)
				pdb.gimp_message("Se ha borrado el pincel  //"+str(brush)+"//  y su imagen origen.")
			else:
				pdb.gimp_message("El pincel //"+str(brush)+"//  NO fue borrado.")
			pdb.gimp_image_delete(img)
		else:
			pdb.gimp_message("El pincel //"+str(brush)+"//  no es editable.")
	
if __name__ == '__main__':

	register(
		"Borrar_Pincel_editable",
		"Borra el pincel activo y su imagen origen (solo para los pinceles creados con los scripts -Pincel activo a pincel editable-, -Imagen activa a pincel editable- o -Imagen en disco a pincel editable-, sus nombres comienzan con (E)).",
		"Borrar Pincel editable",
		"Tanda",
		"Tanda",
		"2008",	
		"<Image>/Pinceles/01-Editar pinceles/05-Borrar pincel editable",
		"RGB*, GRAY*",
		[
			(PF_RADIO, "borrado", "borrar" , 0, (("No", 0), ("Si", 1))),

		],
		[],
		borrar)

#######################06-Actualizar pinceles.

def act(image, drawable):

		pdb.gimp_brushes_refresh()

if __name__ == '__main__':


	register(
		"actualizar_pinceles",
		"Actualizar pinceles",
		"Actualizar pinceles",
		"Tanda",
		"Tanda",
		"2008",	
		"<Image>/Pinceles/01-Editar pinceles/06-Actualizar pinceles",
		"RGB*, GRAY*",
		[],
		[],
		act)


#######################Ayuda.

def ayuda(image, drawable):

		pdb.gimp_message("""Tanda-GIMP-Python-Fu-EditBrushes-V2.1
------------------------
Este script permite editar los pinceles que fueron creados a partir de imagenes (.gbr). 
Se pueden generar pinceles con estas caracteristicas desde una imagen en disco, desde la imagen activa y desde cualquier pincel que tengamos instalado en Gimp. Hay que tener en cuenta que si bien podemos hacer editable cualquier tipo de pincel, el script actualmente solo da como resultado un pincel del tipo .gbr, quiere decir que si convertimos un pincel animado el resultado no sera el esperado. 
Para poder diferenciarlos, el nombre de los pinceles sera el que se haya elegido junto con la extension y el ancho maximo que se podra alcanzar al editarlo y comenzara con (E).
Al crear un pincel se genera una imagen origen dentro de la carpeta -editable- de los pinceles de Gimp (ver en preferencias --- carpetas --- brochas). Para que el script funcione solo debe estar tildada como editable una sola carpeta de todas las disponibles. 
El script usa la imagen origen cada vez que editemos el pincel con lo cual podemos editarlo todas las veces que queramos sin perder calidad.
Hay que tener en cuenta que el tama&o maximo de nuestro pincel estara dado por la resolucion de la imagen origen, es decir que podemos crear pinceles mas grandes pero teniendo en cuenta que pasando el 100 % perderemos definicion.
La imagen origen la podemos editar accediendo a ella con el script -ver o editar imagen origen- una vez que terminemos de editarla sobrescribimos los cambios "ctrl+s" y la proxima vez que editemos nuestro pincel se actualizara, si en la edicion se aumento la resolucion, para que se actualice en el nombre del pincel se tiene que cambiar el nombre del mismo con el script -Renombrar pincel-.
Para eliminar alguno de los pinceles creados se debe hacer utilizando el script -Borrar pincel editable- de esta manera no solo se borra el pincel sino que tambien su imagen origen. De la misma manera para duplicar o renombrar un pincel se deben usar los scripts -Duplicar pincel editable- o -Renombrar pincel editable-.
El Script fue testeado en Linux con Gimp 2.2.x y 2.4.x y funciona correctamente.
..............................
http://lodetanda.blogspot.com -- lodetanda @ gmail.com
------------------------""")

if __name__ == '__main__':


	register(
		"Ayuda",
		"Ayuda",
		"Ayuda",
		"Tanda",
		"Tanda",
		"2008",	
		"<Image>/Pinceles/Ayuda",
		"RGB*, GRAY*",
		[],
		[],
		ayuda)

	main()
