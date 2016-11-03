#!/usr/bin/python
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, Oct 2016
#

import math
from PIL import Image
from numpy import *
from scipy.ndimage import filters
from scipy.misc import imsave
import sys

# calculate "Edge strength map" of an image
#
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return filtered_y**2

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_edge(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( max(y-thickness//2, 0), min(y+thickness//2, image.size[1]-1 ) ):
            image.putpixel((x, t), color)
    return image


def get_best_col_val (edge_strength):
	"""
	Get the best value for this column and then store the index
	to mark that value as the best.
	1.) To Calulate Sub Part - I
	"""
	best = []
	no_of_cols = edge_strength.shape[1]
	for each_col in range(no_of_cols):
		best.append(argmax(edge_strength[:,each_col]))
	return best

def using_mcmc (edge_strength):
	"""
	Get the best value for this column based on the previous decision
	2.) To calculate Sub Part - II
	"""

	best = [argmax(edge_strength[:,0])]
	#best = [152]
	no_of_cols = edge_strength.shape[1]
	print(best)
	for each_col in range(1,no_of_cols):
		best.append(get_best(best[each_col - 1],edge_strength[:,each_col]))
	return best

def get_best (previous_value, col_data):

	maximum = col_data.max()
	probabilities = []
	for each_item in range(len(col_data)):
		probabilities.append((col_data[each_item]/maximum) * distance(previous_value, each_item))
		#print(col_data[each_item]/maximum)

	return argmax(probabilities)

def distance (previous_value, each_item):

	simple_distance = math.fabs(previous_value - each_item)
	if (simple_distance != 0): return 1/simple_distance
	else: return 1

# main program
#
(input_filename, output_filename, gt_row, gt_col) = sys.argv[1:]

# load in image 
input_image = Image.open(input_filename)

# compute edge strength mask
edge_strength = edge_strength(input_image)
mcmc = using_mcmc(edge_strength)
print(mcmc)
best = get_best_col_val(edge_strength)
imsave('edges.jpg', edge_strength)

# You'll need to add code here to figure out the results! For now,
# just create a horizontal centered line.
ridge = [ edge_strength.shape[0]//2 ] * edge_strength.shape[1]
# output answer
imsave(output_filename, draw_edge(input_image, best, (255, 0, 0), 5))
imsave(output_filename, draw_edge(input_image, mcmc, (0, 0, 255), 5))
