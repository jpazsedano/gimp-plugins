#!/usr/bin/env python

from gimpfu import *

def resize_ig(img, blurvalue):
	# Maybe the current image is got by parameter?
	#img = gimp.image_list()[0]

	# This allows to undo everything with just one undo.
	pdb.gimp_undo_push_group_start(img)

	# Rescale the image to be square
	if img.height > img.width:
		img.resize(img.height, img.height, (img.height - img.width) / 2)
	else:
		img.resize(img.width, img.width, 0, (img.width - img.height) / 2)
	
	# Insert a second layer with a copy of the contents and get current background layer
	img.insert_layer(img.layers[0].copy())
	l = img.layers[-1]
	if l.height > l.width:
		resize_factor = float(l.height) / float(l.width)
		pdb.gimp_layer_scale(l, l.height, int(l.height * resize_factor), True)
	else:
		resize_factor = float(l.width) / float(l.height)
		pdb.gimp_layer_scale(l, int(l.width * resize_factor), l.width, True)
	
	# Apply a gaussian blur to the background layer
	pdb.plug_in_gauss(img, l, blurvalue, blurvalue, 0)
	# And rescale the image to be 1080x1080 for instagram.
	img.scale(1080, 1080)

	pdb.gimp_undo_push_group_end(img)

register(
    "python_fu_resize_ig",
    "Resize to IG res",
    "Resize the image to the starndard 1080x1080 IG resolution, with blur background",
    "Javier Paz Sedano",
    "Javier Paz Sedano",
    "2020",
    "Resize to IG...",
    "*",
    [
        (PF_IMAGE, 'img', 'Input image', None),
        (PF_INT, "blurvalue", "Blur value", 50)
    ],
    [],
    resize_ig, menu="<Image>/Filters/Generic")

main()




