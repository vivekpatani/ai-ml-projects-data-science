#Ridge Detection using Markov Chain Monte Carlo

##DOCUMENTATION:

###HMM Formulation:

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

 - To run: ```python mountain.py test_images/mountain.jpg output.jpg 152 171```
 - mountain.py - Script
 - test_images/mountain.py - Test Image
 - output.jpg - Output Image name
 - X coordinate on the ridge in the image
 - Y Coordinate