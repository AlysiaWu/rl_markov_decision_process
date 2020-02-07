import mdptoolbox.example
import numpy as np


# Calculate States
# the number of sides of the die
n_sides=6

# the number of rolls of the die
n_runs = 3

# the number of actions
n_actions = 2

# the number of total states
n_states = n_runs * n_sides + 2  # from 0 to 2N, plus quit

# the boolean mask to indicate which states you will loose money on
isBadSide= np.array([1,1,1,0,0,0])
isGoodSide = [not i for i in isBadSide]

# the array which contains the values of the die
die = np.arange(1, n_sides + 1)        # [1, 2, 3, 4, 5, 6]

# the total earnings given a die roll
earnings = die * isGoodSide  # [0, 0, 0, 4, 5, 6]


# Create probability array==========================
prob = np.zeros((n_actions, n_states, n_states))

"""
The number of actions, the number of states, the number of states
2 x 19 x 19

[ [0, 0, ...x19],
  [0, 0, ...x19],
  [0, 0, ...x19]
  ..x19
],[[0, 0, ...x19],
  [0, 0, ...x19],
  [0, 0, ...x19]
]
"""

# the probability that you will not roll the dice, will transition from the same state
np.fill_diagonal(prob[0], 1)

# if roll
# Calculate probability for Input:
p = 1.0 / n_sides

# Create pro_1
# Create 1 X (1+run*N+2) array
zero = np.array([0]).repeat((n_runs - 1) * n_sides + 2) #Don't change it! It must have size= run-1)*N+1
isGoodSide_2 = np.concatenate((np.array([0]), isGoodSide, zero), axis=0) # rbind
# Create 1 X (run*N+3)*3 array
isGoodSide_N = np.concatenate((isGoodSide_2, isGoodSide_2), axis=0)

# Create 1 X ((run*N+3)^2 array
for i in range(0, n_runs * n_sides + 2):
    isGoodSide_N = np.concatenate((isGoodSide_N, isGoodSide_2), axis=0)
    i = i + 1
# Create 1 X (2N+2)^2 array by trancation
isGoodSide_N = isGoodSide_N[:(n_states ** 2)]

isGoodSide_N = isGoodSide_N.reshape(n_states, n_states) # Reshaping (rows first)
prob[1] = np.triu(isGoodSide_N) # upper triangle matirx
prob[1] = prob[1]*p
prob_quit = 1 - np.sum(prob[1, :n_states, :n_states - 1], axis=1).reshape(-1, 1) # last column

prob[1] = np.concatenate((prob[1, :n_states, :n_states - 1], prob_quit), axis=1) #cbind
np.sum(prob[0], axis=1) # test row sum
np.sum(prob[1], axis=1) # test column sum

# Create rewards array==========================

rewards = np.zeros((n_actions, n_states, n_states))
# if leave
rewards[0] = np.zeros((n_states, n_states))

# if roll
# Create roll reward array
# Create 1 X (1+run*N+2) array
#zero = np.array([0]).repeat((run-1)*N+2) #Don't change it! It must have size= run-1)*N+1
dollar_2 = np.concatenate((np.array([0]), earnings, zero), axis=0) # rbind
# Create 1 X (run*N+3)*3 array
dollar_N = np.concatenate((dollar_2, dollar_2), axis=0)
# Create 1 X ((run*N+3)^2 array
for i in range(0, n_runs * n_sides + 2):
    dollar_N = np.concatenate((dollar_N, dollar_2), axis=0)
    i = i + 1
# Create 1 X (2N+2)^2 array by trancation
dollar_N = dollar_N[:(n_states ** 2)]

dollar_N = dollar_N.reshape(n_states, n_states) # Reshaping (rows first)
rewards[1] = np.triu(dollar_N) # upper triangle matirx
rewards[1] = rewards[1]
rewards_quit = - np.array(range(0, n_states)).reshape(-1, 1) #convert vector to n X 1 matrix
rewards[1] = np.concatenate((rewards[1, :n_states, :n_states - 1], rewards_quit), axis=1) #cbind

print(prob)

print(rewards)

vi = mdptoolbox.mdp.ValueIteration(prob, rewards, 1)
vi.run()

optimal_policy = vi.policy
expected_values = vi.V

print optimal_policy
print expected_values
