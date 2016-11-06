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
	for each_col in range(1,no_of_cols):
		best.append(get_best(best[each_col - 1],edge_strength[:,each_col]))
	return best

def using_mcmc_two (edge_strength, sample_size=10):
	"""
	Using randomisation

	"""
	random_sample = {}
	random_sample[0] = get_best_col_val(edge_strength)

	probability_distribution = []

	no_of_cols = edge_strength.shape[1]
	#print(no_of_cols)

	# For each sample
	for t in range(1,sample_size):

			#Select the previous sample for referrence
			previous_sample = random_sample[t-1]
			current_sample = []
			
			#For each column in that image
			for column in range(no_of_cols):

				if (column == 0):
					previous_column = None
					next_column = previous_sample[1]

				elif (column == no_of_cols - 1):
					previous_column = previous_sample[no_of_cols - 2]
					next_column = None

				else:
					previous_column = previous_sample[t-1]
					next_column = previous_sample[t+1]

				#print(previous_column, next_column)

				probability_distribution = probability(previous_column, next_column, edge_strength[:,column])
				probability_distribution = probability_distribution / sum(probability_distribution)
				low_end, high_end = get_bounds(previous_column, next_column, len(edge_strength[:,column]))

				rows = list(range(low_end, high_end))
				s_i = random.choice(rows, p=probability_distribution)
				if (not s_i): print(low_end, high_end)
				current_sample.append(s_i)

			random_sample[t] = current_sample

def get_bounds (previous_column, next_column, maxsize):

	check_range = 5

	if (previous_column == None):
		low_end = next_column - check_range
		high_end = next_column + check_range

	elif (next_column == None):
		low_end = previous_column - check_range
		high_end = previous_column + check_range

	else:
		lower_bound = previous_column if (previous_column < next_column) else next_column
		upper_bound = previous_column if (previous_column > next_column) else next_column
		low_end = lower_bound - check_range
		high_end = upper_bound + check_range

	if (low_end < 0): low_end = 0
	if (high_end > maxsize): high_end = maxsize

	return low_end, high_end

def probability (previous_column, next_column, column_data):

	column_sum = sum(column_data)
	probabilities = []
	
	low_end, high_end = get_bounds(previous_column, next_column, len(column_data))
	
	dist_prev = []
	dist_next = []
	
	if (previous_column == None):
		for row in range(low_end, high_end):
			dist_next.append(math.fabs(row - next_column))

		count = 0
		for row in range(low_end, high_end):
			probabilities.append(column_data[row]/column_sum * math.fabs(dist_next[count])/math.fabs(sum(dist_next)))
			count += 1
	
	elif (next_column == None):
		for row in range(low_end, high_end):
			dist_prev.append(math.fabs(row - previous_column))

		count = 0
		for row in range(low_end, high_end):
			probabilities.append(column_data[row]/column_sum * math.fabs(dist_prev[count])/math.fabs(sum(dist_prev)))
			count += 1

	else:
		for row in range(low_end, high_end):
			dist_prev.append(math.fabs(row - previous_column))
			dist_next.append(math.fabs(row - next_column))

		count = 0
		for row in range(low_end, high_end):
			probabilities.append(math.fabs(dist_prev[count] / sum(dist_prev)) * column_data[row]/column_sum * math.fabs(dist_next[count]/sum(dist_next)))
			count += 1

	return probabilities

def get_best (previous_value, col_data):

	maximum = col_data.max()
	probabilities = []
	for each_item in range(len(col_data)):
		probabilities.append((col_data[each_item]/maximum) * distance(previous_value, each_item))
		#print(col_data[each_item]/maximum)

	return argmax(probabilities)

def distance_two (compare_value, current_value, total_distance):

	distance = math.fabs(compare_value - current_value) / total_distance
	return distance


def distance (previous_value, current_value):

	simple_distance = math.fabs(previous_value - current_value)
	if (simple_distance != 0): 
		#print(1/simple_distance)
		return 1/simple_distance
	return 1

# main program
#
(input_filename, output_filename, gt_row, gt_col) = sys.argv[1:]

# load in image 
input_image = Image.open(input_filename)

# compute edge strength mask
edge_strength = edge_strength(input_image)
imsave('edges.jpg', edge_strength)

# Get the best possible ridge
naive = get_best_col_val(edge_strength)
mcmc = using_mcmc(edge_strength)
mcmc_two = using_mcmc_two(edge_strength)

# You'll need to add code here to figure out the results! For now,
# just create a horizontal centered line.
ridge = [ edge_strength.shape[0]//2 ] * edge_strength.shape[1]
# output answer
imsave(output_filename, draw_edge(input_image, mcmc_two, (255, 0, 0), 5))
#imsave(output_filename, draw_edge(input_image, mcmc, (0, 0, 255), 5))
