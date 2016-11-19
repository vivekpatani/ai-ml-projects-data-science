#!/usr/bin/python3
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, Oct 2016
#


"""

DOCUMENTATION:

* HMM Formulation:

1.) - State - Each state can be a representation of the column, where gradient is the observed variable and we are 
	trying to determine the probability of row being selected

2.) - Hidden Variables - Here in we are considering the hidden variables to be the row numbers.

3.) - Transition Probabilities - This is the probabilities which help us determine a given state, based on its neighbours.
	For us it depends upon the previous and the next state.
	- We look to maximise this factor, to ensure smoothness i.e. keep in mind that the next state is not abrubptly away from
	the current and previous. Hence we focus our search to
	nearest possible neighbours
4.) - Emission Probabilites - This in our problem, is the variable that connects hidden and observed states, this is clearly
	visible to us.
	- We normalise this using the sum of inspected gradients by, dividing the given row gradient by the sum.

* Programme Explanation:

1.) Part I
	- This is simple and is implemented in best_edge_list(edge_length)
	- The idea was to simply pick the best gradient there is and use it for the corresponding column.
	- Keep doing this for each row and you shall have an output.
	- Well, it is not completely efficient, but it is a start.

2.) Part II
	- Implementation I: (implemented in the function mcmc())
		* In this we begin with, a random sample (not completely random, random sample is derieved from the first output)
		* That random sample is then given as input to the programme:
		* Loop this:
		* 		For each col:
		*			calculate the probability of each row based on 3 heuristics (previous state, next_state, gradient)
		*			Normalise it
		*			pick the best row using random choice from the generated distribution
		* The above code is repeatedly run for about 500 times to generate a lot of samples, in the hope to converge the distribution
		* The last state generated is picked and the best output is provided.

	- Implementation II: (implemented in the function mcmc_alternative())
		* In this we pick top k values from column zero
		* In Each Iteration for k times:
		* 	We start with a new starting point from the top k selected
		*	calculate the probability of each row based on 3 heuristics (previous state, next_state, gradient)
		* 	We compute the MAP value here as well
		* After all the samples are generated, we pick the sample with highest MAP and output that.

3.) Part III
	- Implementation: (implemented in the function mcmc_given())
		* We in this case, are following the same method in Part II, Implementation I, with a few changes:
		* We add a fourth heuristic based on the given point i.e. we calculate the proximity of the given point from the current point
		  and then decide whether if lies within immediate vicinity, if it does, we weight it with a simple heuristic which is a product
		  of the inverse of column difference and the inversed square distance difference.

4.) Three Heuristics:
	- previous state - We see how far is the previous selection from the current row using the previous sample data, by calculating the inverse 
	  squared difference.
	- next_state - We see how far is the next selection from the current row using the previous sample data, by calculating the inverse squared
	  difference.
	- gradient - We find the sum of all gradients over a lower_bound and upper_bound, after which we divide each gradient by the devised sum

5.) Misc:
	- In order to limit our search, for each previous and next state consideration we only check a certain offset value, which can be changed.
	- In order to limit our time, we only take 500 samples
	- To run the alternative II, just uncomment line 549 & 550
	- To run the initial input, just uncomment last two lines

"""

from PIL import Image
from numpy import *
from scipy.ndimage import filters
from scipy.misc import imsave
import sys
from multiprocessing.pool import ThreadPool

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
# ===========================================================================================================

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

# =============================================================================================================

def mcmc(edge_strength):
	"""
	Get the best possible value for a ridge using sampling and MCMC
	2.) To Solve Sub Part - II
	"""

	# Basic Defs
	number_of_samples = 100
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

			if (gt_col == i):
				s_i = gt_row
			else:
				s_i = random.choice(rows, p=probability_distribution)
			
			current_sample.append(s_i)

		samples[t] = current_sample

	return samples[number_of_samples - 1]

def probability_calculator (previous_selection, lower_bound, next_selection, upper_bound, column_data):
	"""
	This will calculate the probability of each row for given configuration
	"""
	distance_dist = []
	other_distance_dist = []
	distribution = []
	gradient_dist = []
	col_sum = 0

	#Calculate the row sum for a given column range
	for each_item in range(lower_bound, upper_bound):
		col_sum += column_data[each_item]

	# If this is column 0
	if (previous_selection == None):
		for each_row in range(lower_bound, upper_bound):
			distance_dist.append(transition(next_selection, each_row))
			gradient_dist.append(emission(column_data[each_row], col_sum))

		for each_item in range(len(distance_dist)):
			distribution.append(distance_dist[each_item] * gradient_dist[each_item])

	# If this is column n-1
	elif (next_selection == None):
		for each_row in range(lower_bound, upper_bound):
			distance_dist.append(transition(previous_selection, each_row))
			gradient_dist.append(emission(column_data[each_row], col_sum))

		for each_item in range(len(distance_dist)):
			distribution.append(distance_dist[each_item] * gradient_dist[each_item])

	# Else any other row.
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
	# When both lie on the same line.
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
	offset = 20

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

# =================================================================================================

def mcmc_alternative (edge_strength):
	"""
	Alternative MCMC
	"""
	k = 250
	init_data = top_k_indices(edge_strength[:,0], k)
	sample = {}
	map_values = zeros(k)
	sample[0] = best_edge_list(edge_strength)

	# Do this k times.
	for each_sample in range(len(init_data)):

		# Select the best possible starting point.
		best = []
		best.append(init_data[each_sample])
		total = 0

		# Number of columns
		number_of_cols = edge_strength.shape[1]
		
		# For each column, find the best row
		for each_col in range(1, number_of_cols):
			current, map_val = probability_calculator_alt(best[each_col - 1], edge_strength[:,each_col], each_col)
			best.append(current)
			total += map_val

		sample[each_sample] = best
		map_values[each_sample] = total

	output = sample[argmax(map_values)]

	return output

def probability_calculator_alt (previous_selection, column_data, column_number):
	"""
	Calculates probabilites for all rows and then returns the best selection
	"""
	posteriors = []
	lower_bound, upper_bound = get_bounds_alt(previous_selection, len(column_data))

	col_sum = 0
	for each_row in range(lower_bound, upper_bound):
		col_sum += column_data[each_row]

	for each_row in range(lower_bound, upper_bound):

		if (column_number == gt_col and each_row == gt_row):
			transition_probability = 1
			emission_probability = 1
		else:
			transition_probability = transition(previous_selection, column_data[each_row])
			emission_probability = emission(column_data[each_row], col_sum)
		
		posteriors.append(emission_probability * transition_probability)

	return argmax(posteriors) + lower_bound, max(posteriors)

def get_bounds_alt (previous_selection, maxsize):
	"""
	Get bounds for a certain selection, to scan the current column within a range.
	"""
	offset = 7

	lower_bound = previous_selection - offset
	upper_bound = previous_selection + offset

	if (lower_bound < 0): lower_bound = 0
	if (upper_bound > maxsize): upper_bound = maxsize

	return lower_bound, upper_bound


def top_k_indices (init_data, k = 50):
	"""
	Returns the top k begining indexes based on value
	"""
	indices = argpartition(init_data, -k)[-k:]
	return indices


# =================================================================================================

# =================================================================================================

def mcmc_given (edge_strength, gt_row, gt_col):
	"""
	Given a certain point, find the ridge line.
	3.) Solve sub part - III
	"""
	# Basic Defs
	number_of_samples = 100
	no_of_cols = edge_strength.shape[1]

	# Generate a random Sample
	random_sample = best_edge_list(edge_strength)
	random_sample[gt_col] = gt_row

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
			probability_distribution = probability_calculator_given(previous_selection, lower_bound, next_selection, upper_bound, edge_strength[:,i], gt_row, gt_col, i)
			probability_distribution = normalise(probability_distribution)

			rows = arange(lower_bound, upper_bound)

			if (gt_col == i):
				s_i = gt_row
			else:
				s_i = random.choice(rows, p=probability_distribution)
			
			current_sample.append(s_i)

		samples[t] = current_sample

	output = find_mode(samples)

	return output

def probability_calculator_given (previous_selection, lower_bound, next_selection, upper_bound, column_data, gt_row, gt_col, column_number):
	"""
	This will calculate the probability of each row for given configuration
	"""

	distribution = []
	
	# 4 parameters
	distance_dist = []
	other_distance_dist = []
	gradient_dist = []
	given_dist = []

	col_sum = 0

	#Calculate the row sum for a given column range
	for each_item in range(lower_bound, upper_bound):
		col_sum += column_data[each_item]

	# If this is column 0
	if (previous_selection == None):
		for each_row in range(lower_bound, upper_bound):
			distance_dist.append(transition(next_selection, each_row))
			gradient_dist.append(emission(column_data[each_row], col_sum))
			given_dist.append(near_heuristic(column_number, gt_col, each_row, gt_row))

		for each_item in range(len(distance_dist)):
			distribution.append(distance_dist[each_item] * gradient_dist[each_item] * given_dist[each_item])

	# If this is column n-1
	elif (next_selection == None):
		for each_row in range(lower_bound, upper_bound):
			distance_dist.append(transition(previous_selection, each_row))
			gradient_dist.append(emission(column_data[each_row], col_sum))
			given_dist.append(near_heuristic(column_number, gt_col, each_row, gt_row))

		for each_item in range(len(distance_dist)):
			distribution.append(distance_dist[each_item] * gradient_dist[each_item] * given_dist[each_item])

	# Else any other row.
	else:
		for each_row in range(lower_bound, upper_bound):
			distance_dist.append(transition(next_selection, each_row))
			other_distance_dist.append(transition(previous_selection, each_row))
			gradient_dist.append(emission(column_data[each_row], col_sum))
			given_dist.append(near_heuristic(column_number, gt_col, each_row, gt_row))

		for each_item in range(len(distance_dist)):
			distribution.append(distance_dist[each_item] * gradient_dist[each_item] * other_distance_dist[each_item] * given_dist[each_item])

	return distribution

def near_heuristic (column_number, gt_col, row_number, gt_row):
	"""
	Calculate how far is the given point away from user feedback
	"""
	offset = 15
	if (math.fabs(column_number - gt_col) < offset and math.fabs(column_number - gt_col) != 0):
		return (distance(row_number, gt_row) * (1 / math.fabs(column_number - gt_col)))
	return 1

def distance (row_number, gt_row):
	"""
	Returns a distance heuristic to weigh the nearness to user feedback
	"""

	# If the difference is really less
	if ((row_number - gt_row) == 0): return 0.99
	return 1 / math.fabs(row_number**2 - gt_row**2)

def find_mode (samples):
	"""
	Finds the modes of the given sample collection
	"""
	output = []
	space = array(list(zip(*samples.values())))
	for each_sample in space:
		current = bincount(each_sample)
		output.append(argmax(current))

	return output
	

	return output
# ===================================================================================================
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
# part 0
# for rows in range(len(ridge)):
# 	ridge[rows] = 152

part1 = best_edge_list(edge_strength)
imsave(output_filename, draw_edge(input_image, part1, (255, 0, 0), 5))

part2 = mcmc(edge_strength)
imsave(output_filename, draw_edge(input_image, part2, (0, 0, 255), 5))

# part2alt = mcmc_alternative(edge_strength)
# imsave(output_filename, draw_edge(input_image, part2alt, (0, 0, 255), 5))

part3 = mcmc_given (edge_strength, int(gt_row), int(gt_col))
imsave(output_filename, draw_edge(input_image, part3, (0, 255, 0), 5))

# output answer
# imsave(output_filename, draw_edge(input_image, ridge, (255, 0, 0), 5))