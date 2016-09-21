#!/usr/bin/env python

#Script in Python for The Gimp, this script allows you to generate, delete, duplicate and EDIT brushes generated from images or of other brush.

#Copyright (c) (2008) Marcelo "Tanda" Cervi&o.
#Argentina. 
# http://lodetanda.blogspot.com -- lodetanda @ gmail.com

# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

#You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

#Tanda-GIMP-Python-Fu-EditBrushes-V2.1 ----03/2008----.
#Hosted in github ----09/2016----.


from gimpfu import *
import os

##################01-Edit brush.

def editar(image, drawable, porcentaje, aspectox, aspectoy, angulo, esp, flip):

		
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
			pdb.gimp_message("The brush //"+str(brush)+"// is not editable")

if __name__ == '__main__':

	register(
		"Edit_brush",
		"Modify the properties of any brush made with the scripts -Active brush to edit brush-, -Active Image to edit brush- or -Image in disc to edit brush-, their names begin with (E).",
		"Edit brush",
		"Tanda",
		"Tanda",
		"2008",	
		"<Image>/Brushes/01-Edit brushes/01-Edit brush",
		"RGB*, GRAY*",
		[
			(PF_SPINNER, "porcentaje", "Diameter %", 20, (1, 500, 1)),
			(PF_SPINNER, "aspectox", "proportionX %", 100, (1, 100, 1)),
			(PF_SPINNER, "aspectoy", "proportionY %", 100, (1, 100, 1)),
			(PF_SPINNER, "angulo", "Angle", 0, (-360, 360, 1)),
			(PF_SPINNER, "esp", "Spacing", 15, (1, 5000, 1)),
			(PF_RADIO, "flip", "Flip", 2, (("Horizontal", 0), ("Vertical", 1), ("Neither", 2))),
		],
		[],
		editar)

##################02-see or edit source image.

def origen(image, drawable):

		
		ruta_pinceles = pdb.gimp_gimprc_query("brush-path-writable")
		brush = pdb.gimp_context_get_brush()
		archivos = os.listdir(ruta_pinceles)
		imagen_origen = ruta_pinceles+os.sep+brush

		if brush+'(brush)'+'.gbr' and brush in archivos:

				img = pdb.gimp_file_load(imagen_origen, imagen_origen)
				pdb.gimp_display_new (img)
				pdb.gimp_message("The source image belonging to the brush //"+str(brush)+"// have already been opened, once you have made the changes you have to save them with -ctrl+s- and the next time you edit this brush they will be updated. If in the edition the resolution have been increased, to update the brush name, you will have to change the name with the script -Rename brush-.")
		else:
			pdb.gimp_message("The brush //"+str(brush)+"//  does not have source image because it is NOT editable.")
			
		
if __name__ == '__main__':


	register(
		"See_or_edit_source_image",
		"See or edit the source image of the active brush.    Tanda.",
		"See or edit source image",
		"Tanda",
		"Tanda",
		"2008",	
		"<Image>/Brushes/01-Edit brushes/02-See or edit source image",
		"RGB*, GRAY*",
		[],
		[],
		origen)

################01- active brush to edit brush

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
	pdb.gimp_message("A new editable brush has been created whose name is    "+str(nombre_pincel))

if __name__ == '__main__':

	register(
		"active_brush_to_edit_brush",
		"Make a brush from the active brush, that then will be able to edit with the script -Edit Brush-.",
		"active brush to edit brush",
		"Tanda",
		"Tanda",
		"2008",		
		"<Image>/Brushes/02-Create edit brushes/01-Active brush to edit brush",
		"RGB*, GRAY*",
		[
			(PF_STRING, "nombre", "Name", ""),
			(PF_RADIO, "guardarcomo", "Save source image as", ".png", ((".png", ".png"), (".jpg", ".jpg"))),
			(PF_SPINNER, "porcentaje", "Diameter %", 100, (1, 500, 1)),
			(PF_SPINNER, "esp", "Spacing", 15, (1, 5000, 1)),
			(PF_RADIO, "colorbrush", "Paint with:", 1, (("image color", 0), ("choose color", 1))),
			(PF_RADIO, "fixrotacion", "Scale for fix rotate", 0, (("no", 0), ("si", 1))),
		],
		[],
		actual)

##############02-Active Image to edit brush.

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
	pdb.gimp_message("A new editable brush has been created whose name is    "+str(nombre_pincel))
	
if __name__ == '__main__':

	register(
		"active_image_to_edit_brush",
		"Make a brush from the active image, that then will be able to edit with the script -Edit Brush-.",
		"active image to edit brush",
		"Tanda",
		"Tanda",
		"2008",		
		"<Image>/Brushes/02-Create edit brushes/02-Active Image to edit brush",
		"RGB*, GRAY*",
		[
			
			(PF_STRING, "nombre", "Name", ""),
			(PF_RADIO, "guardarcomo", "save source image as", ".png", ((".png", ".png"), (".jpg", ".jpg"))),
			(PF_SPINNER, "porcentaje", "Diameter %", 20, (1, 500, 1)),
			(PF_SPINNER, "angulo", "Angle", 0, (-360, 360, 1)),
			(PF_SPINNER, "esp", "Spacing", 15, (1, 5000, 1)),
			(PF_RADIO, "colorbrush", "Paint with:", 3, (("image color", 2), ("choose color", 3))),
			(PF_RADIO, "fixrotacion", "Scale for fix rotate", 0, (("no", 0), ("si", 1))),
		],
		[],
		crear_img_sel)

###################03- Image in disc to edit brush.

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
	pdb.gimp_message("A new editable brush has been created whose name is    "+str(nombre_pincel))

	
if __name__ == '__main__':

	register(
		"image_in_disc_to_edit_brush",
		"Make a brush from the image in disc, that then will be able to edit with the script -Edit brush-.",
		"image in disc to edit brush",
		"Tanda",
		"Tanda",
		"2008",		
		"<Image>/Brushes/02-Create edit brushes/03-Image in disc to edit brush",
		"RGB*, GRAY*",
		[
			(PF_FILE, "ruta", "image", ""),
			(PF_RADIO, "guardarcomo", "Save source image as", ".png", ((".png", ".png"), (".jpg", ".jpg"))),
			(PF_STRING, "nombre", "Name", ""),
			(PF_SPINNER, "porcentaje", "Diameter %", 20, (1, 500, 1)),
			(PF_SPINNER, "angulo", "Angle", 0, (-360, 360, 1)),
			(PF_SPINNER, "esp", "Spacing", 15, (1, 5000, 1)),
			(PF_RADIO, "colorbrush", "Paint with:", 1, (("image color", 0), ("choose color", 1))),
			(PF_RADIO, "fixrotacion", "Scale for fix rotate", 0, (("no", 0), ("si", 1))),
		],
		[],
		crear_de_ruta)
	
###############03-Duplicate edit brush.

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
			pdb.gimp_message("A new editable brush has been created whose name is  "+str(brush))
		else:
			pdb.gimp_message("The brush could not be duplicate.")
			pdb.gimp_context_set_background(fondo_original)
			pdb.gimp_image_delete(img)

	else:
		pdb.gimp_message("The brush //"+str(brush)+"// it is not editable.")
	
if __name__ == '__main__':

	register(
		"Duplicate_edit_brush",
		"Duplicate the active brush and its source image (only for the brushes made with the scripts -Active brush to edit brush-, -Active Image to edit brush- or -Image in disc to edit brush-, their names begin with (E)).",
		"Duplicate Edit Brush",
		"tanda",
		"tanda",
		"2008",	
		"<Image>/Brushes/01-Edit brushes/03-Duplicate edit brush",
		"RGB*, GRAY*",
		[
			(PF_RADIO, "duplicar", "Duplicate", 0, (("No", 0), ("Yes", 1))),

		],
		[],
		duplicar)

###############04-Rename edit brush.

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
			pdb.gimp_message("his brush now is called   "+str(nombre_pincel))
			pdb.gimp_context_set_background(fondo_original)
			pdb.gimp_image_delete(img)
		else:
			pdb.gimp_message("The brush //"+str(brush)+"// it is not editable.")

if __name__ == '__main__':

	register(
		"Rename_Edit_Brush",
		"Rename the active edit brush and its source image (only for the brushes made with the scripts -Active brush to edit brush-, -Active Image to edit brush- or -Image in disc to edit brush-, their names begin with (E)).",
		"Rename edit brush",
		"Tanda",
		"Tanda",
		"2008",	
		"<Image>/Brushes/01-Edit brushes/04-Rename edit brush",
		"RGB*, GRAY*",
		[
			(PF_STRING, "renombre", "Name new", ""),

		],
		[],
		renombrar)

###############05-Delete edit brush.

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
				pdb.gimp_message("it was deleted The brush  //"+str(brush)+"//  and his source image.")
			else:
				pdb.gimp_message("The brush //"+str(brush)+"//  it was not deleted.")
			pdb.gimp_image_delete(img)
		else:
			pdb.gimp_message("The brush //"+str(brush)+"// it is not editable.")
	
if __name__ == '__main__':

	register(
		"Delete_edit_brush",
		"Delete the active edit brush and its source image (only for the brushes made with the scripts -Active brush to edit brush-, -Active image to edit brush- or -Image in disc to edit brush-, their names begin with (E)).",
		"Borrar Pincel",
		"Tanda",
		"Tanda",
		"2008",	
		"<Image>/Brushes/01-Edit brushes/05-Delete edit brush",
		"RGB*, GRAY*",
		[
			(PF_RADIO, "borrado", "Delete" , 0, (("No", 0), ("Yes", 1))),

		],
		[],
		borrar)

#######################06-Update brushes.

def act(image, drawable):

		pdb.gimp_brushes_refresh()

if __name__ == '__main__':


	register(
		"Update_brushes",
		"Update brushes",
		"Update brushes",
		"Tanda",
		"Tanda",
		"2008",	
		"<Image>/Brushes/01-Edit brushes/06-Update brushes",
		"RGB*, GRAY*",
		[],
		[],
		act)


#######################Help.

def ayuda(image, drawable):

		pdb.gimp_message("""Tanda-GIMP-Python-Fu-EditBrushes-V2.1
------------------------
This script allows you to edit the brushes that have been made from the images (.gbr).
Brushes with these features can be generated from a disc image, from the active image or any brush that we have installed in Gimp. 
It is necessary to consider that although we can make editable any type of brush, the script at the moment only gives a brush of the type .gbr, it means that if we convert an animated brush the result will not be the awaited one. 

The name of the brushes will be the chosen name with the extension and the maximal width you reach to edit it and it will start with (E). When you create a brush, a source image will be created in a folder -editable- from Gimp brushes (see preferences---folders---brushes). To make the script works, only one folder must be checked as editable. The script uses the souce image each time we edit the brush with which we can edit it every time we want without losing quality.  It is necessary to consider that the maximum size of our brush will be given by the resolution of the source image, that is that we can create bigger brushes but considering that passing 100 % we will lose definition.
The source image we can edit it acceding to it with the script -See or edit source image- once we have finished editing it, we overwrite the changes "ctrl+s" and the next time we edit our brush it will be updated, if in the edition the resolution have been increased, to update the brush name you will have to change the name with the script - Rename Brush-.
To delete some created brushes you must use the script -Delete edit brush-, so that you delete the brush and its source image.  In the same way, to duplicate or rename a brush you must use the script -Duplicate edit brush- or -Rename edit brush.

The script has been tested on Linux with Gimp 2.2.x y 2.4.x and it works correctly.
..............................
http://lodetanda.blogspot.com -- lodetanda @ gmail.com
------------------------""")

if __name__ == '__main__':


	register(
		"Help",
		"Help",
		"Help",
		"Tanda",
		"Tanda",
		"2008",	
		"<Image>/Brushes/Help",
		"RGB*, GRAY*",
		[],
		[],
		ayuda)

	main()
