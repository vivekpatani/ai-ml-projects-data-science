#!/usr/bin/python
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, Oct 2016
#

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


# This is where our code begins

def best_edge_list (edge_strength):
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

def mcmc(edge_strength):
	"""
	Get the best possible value for a ridge using sampling and MCMC
	2.) To Solve Sub Part - II
	"""

	# Basic Defs
	number_of_samples = 50
	no_of_cols = edge_strength.shape[1]

	# Generate a random Sample
	random_sample = best_edge_list(edge_strength)

	# Create a dictionary of samples
	samples = {}
	samples[0] = random_sample

	# Let us now run a number of samples
	for t in range(1, number_of_samples):

		# Choose Previous Sample
		previous_sample = samples[t-1]
		current_sample = []

		# Go through each column of the image.
		for i in range(no_of_cols):

			# If it is column 0
			if (i == 0):
				previous_selection = None
				next_selection = previous_sample[i + 1]

			# If it is column 501
			elif (i == no_of_cols - 1):
				previous_selection = previous_sample[i - 1]
				next_selection = None

			# Else any other column
			else:
				previous_selection = previous_sample[i - 1]
				next_selection = previous_sample[i + 1]

			lower_bound, upper_bound = get_bounds(previous_selection, next_selection, len(edge_strength[:,i]))

			#Calculate the probability distribution
			probability_distribution = probability_calculator(previous_selection, lower_bound, next_selection, upper_bound, edge_strength[:,i])
			probability_distribution = normalise(probability_distribution)

			rows = arange(lower_bound, upper_bound)

			s_i = random.choice(rows, p=probability_distribution)
			current_sample.append(s_i)

		samples[t] = current_sample

	return samples[49]

def probability_calculator (previous_selection, lower_bound, next_selection, upper_bound, column_data):
	"""
	This will calculate the probability of each row for given configuration
	"""
	distance_dist = []
	other_distance_dist = []
	distribution = []
	gradient_dist = []
	col_sum = 0

	for each_item in range(lower_bound, upper_bound):
		col_sum += column_data[each_item]

	if (previous_selection == None):
		for each_row in range(lower_bound, upper_bound):
			distance_dist.append(transition(next_selection, each_row))
			gradient_dist.append(emission(column_data[each_row], col_sum))

		for each_item in range(len(distance_dist)):
			distribution.append(distance_dist[each_item] * gradient_dist[each_item])

	elif (next_selection == None):
		for each_row in range(lower_bound, upper_bound):
			distance_dist.append(transition(previous_selection, each_row))
			gradient_dist.append(emission(column_data[each_row], col_sum))

		for each_item in range(len(distance_dist)):
			distribution.append(distance_dist[each_item] * gradient_dist[each_item])

	else:
		for each_row in range(lower_bound, upper_bound):
			distance_dist.append(transition(next_selection, each_row))
			other_distance_dist.append(transition(previous_selection, each_row))
			gradient_dist.append(emission(column_data[each_row], col_sum))

		for each_item in range(len(distance_dist)):
			distribution.append(distance_dist[each_item] * gradient_dist[each_item] * other_distance_dist[each_item])

	return distribution

def transition (value1, value2):
	"""
	Generates the transition probabilities for a row.
	"""
	distance = math.fabs(value1**2 - value2**2)
	if (distance!=0): return 1/distance
	else: return 1

def emission (current_data, total):
	"""
	Generates Emission probability based on Gradient
	"""
	return current_data/total

def normalise (probability_distribution):
	"""
	Coverts a probability distribution to a normalised one.
	"""
	distribution = []

	total = sum(probability_distribution)
	for each_item in probability_distribution:
		distribution.append(each_item / total)

	return distribution

def get_bounds (previous_selection, next_selection, maxsize):
	"""
	Get the bounds for a certain row, by +n and -n
	Handle edge cases as well.
	"""
	offset = 5

	if (previous_selection == None):
		lower_bound = next_selection - offset
		upper_bound = next_selection + offset

	elif (next_selection == None):
		lower_bound = previous_selection - offset
		upper_bound = previous_selection + offset

	else:
		if (previous_selection < next_selection): lower_bound = previous_selection - offset
		else: lower_bound = next_selection - offset

		if (previous_selection > next_selection): upper_bound = previous_selection + offset
		else: upper_bound = next_selection + offset

	if lower_bound < 0: lower_bound = 0
	if upper_bound > maxsize: upper_bound = maxsize

	return lower_bound, upper_bound

# This is where our code ends


# main program
#
(input_filename, output_filename, gt_row, gt_col) = sys.argv[1:]

# load in image 
input_image = Image.open(input_filename)

# compute edge strength mask
edge_strength = edge_strength(input_image)
imsave('edges.jpg', edge_strength)

# You'll need to add code here to figure out the results! For now,
# just create a horizontal centered line.
ridge = [ edge_strength.shape[0]//2 ] * edge_strength.shape[1]

# My Calls
part1 = best_edge_list(edge_strength)
imsave(output_filename, draw_edge(input_image, part1, (255, 0, 0), 5))

part2 = mcmc(edge_strength)
imsave(output_filename, draw_edge(input_image, part2, (0, 0, 255), 5))

# output answer
#imsave(output_filename, draw_edge(input_image, ridge, (255, 0, 0), 5))