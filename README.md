# Markov Decision Process using Value Iteration

This notebook provides a simple example of how to setup an MDP and use Value Iteration to find the optimal policy and the expected values at each state.

## Requirements

- pymdptoolbox only supports python 2.7, 3.2, 3.3, 3.4
- Install dependencies jupyter, pymdptoolbox, and numpy

## Quick Start
```
pip install -r requirements.txt
jupyter notebook pymdptoolbox_DieN.ipynb
```

## The Game
The game DieN is played in the following way:

1.  You will be given a die with ​ N ​ sides. You will know the size of ​ N ​ , and can assume that N is a value greater than 1 and less than or equal to 30.

2. You will be given a boolean mask vector: isBadSide where the value of 1 indicates the sides of the die that will make you lose. 
The vector will be of size ​ N.

3. You start with 0 dollars.

4. At any time you have the option to roll the die or to quit the game
  
    a. If you decide to roll:
   
   i.  And you roll a number not in: isBadSide, ​ you receive that many dollars. (eg. if you roll the number 2 and 2 is not  a bad side -- meaning the second element of the vector is 0 -- in ​ isBadSide , ​ then you receive 2 dollars)
Repeat step 4.

    ii.  And you roll a number in ​ isBadSide, ​ then you lose all money obtained in previous rolls and the game ends.
  
    b. If you decide to quit:
    i.  You keep all the money gained from previous rolls and the game ends.
    
### A Simple Example: Coin Toss
The state transition diagram is shown below for a simple heads tails game using these rules.  Here a coin can be modeled as
a die roll of two sides.  There are two actions you can take in each state.  You can roll the dice or quit.
If you quit, there is a 100% chance that you will transition to the end state getting whatever reward you have accumulated.
If you roll the dice, there is a 50% chance that you will go to the terminal state and lose all your money, and a 50%
chance that you will get 1 reward.

As shown below, the states are the circles and represent how much money you have earned.  The links are the
transitions, each transition has an action associated with it, probability associated with it, and a reward
if executed.

![markov example](./markov.png)

### Procedure
For this problem, determine an optimal policy for playing the game DieN for ​ N ​ sides. You
will be given ​ N ​ and the array ​ isBadSide ​ which indicates which sides are bad. As you will see, the optimal policy for this game will depend on ​ your current bankroll.

What is the expected amount of dollars for this game if you follow an optimal policy? That
is, what is the optimal state-value function for the initial state of the game? Provide
answers for the problems you are given on Canvas. Your answer must be correct to 3
decimal places.

Examples

The following examples can be used to verify your calculation is correct.

● Input: N = 21, isBadSide = [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0], Output: 7.379

● Input: N = 22, isBadSide = [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0], Output: 6.314

● Input: N = 6, isBadSide = [1, 1, 1, 0, 0, 0], Output: 2.583

### Approach
Please see the jupyter notebook on a detailed breakdown on how to solve this game.

### Resources and References:

Littman and Isbel.  Georgia Tech University: Reinforcement Learning.

Mdptoolbox.  https://pymdptoolbox.readthedocs.io/en/latest/api/mdptoolbox.html

open pymdp_DieN.py, change inital setting according to the question.
For example
Input: N = 6, isBadSide = {1,1,1,0,0,0}, Output: 2.5833


## Contribute

If you have suggestions for improvements or bug fixes, feel free to submit a [pull request](https://help.github.com/articles/creating-a-pull-request/) or create an [issue](https://github.com/rldm/rldm_tutorials/issues).

