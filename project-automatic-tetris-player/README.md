#AUTOMATIC TETRIS AI:

#Problem Statement:
 - Automate the process of playing tetris - leave that on us. You will win, trust me!
 - Maximise the score, even though you might not reach infinite points because distribution isn't absolutely random, it is quite a bit too random I guess.

#Approach:   
 - We have built the Tetris AI bot by making use of the genetic algorithms and minimax. The 
things we took in to consideration were,  
    -  Height   
    -  Bumpiness   
    -  Number of Holes   
    -  Altitude   
    -  Completed Lines   

 - We first look at all the possible places where a piece can be placed with all kinds of orientation, 
then we consider the next piece and place it in all the possible places in all orientation. We 
calculate the score based on this formula, 
Score = a * Height + b * Bumpiness + c * Number of holes + d * Completed lines 
 
 - We calculate the score based on the above formula for each position of the next piece with 
respect to the position of the current piece. We take the final score at the End. 
 
 - We ran a fitness function that gave me the best possible values for the constants a, b, c, d. 
The factor Height is undesirable and we give it a maximum penalty, whereas the Completed 
Lines is a very desirable thing to have and hence we reward it by a positive number.  
 
 - The feature Number of Holes and Bumpiness are undesirable too, therefore we penalize it. 
After trying different values, the bot started playing well for these values, 
 
 - ```a = -1.5, b = -1.5, c = -3 and d = 4.5 ```
 
 - While Testing the bot performed exceedingly well by crossing 50K mark more than thrice. It 
succumbs to random distribution once in a while.

 - ```skeragod``` collabaration