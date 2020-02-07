import mdptoolbox.example
import numpy as np

class MDP_Domain(object):
    def __init__(self, n_sides, n_runs, n_actions, n_initial_terminal_states):
        self.n_sides = n_sides
        self.n_runs = n_runs
        self.n_actions = n_actions
        self.n_initial_terminal_states = n_initial_terminal_states
        self.n_states = n_runs * n_sides + n_initial_terminal_states

    def create_state_transistions(self, reachable, unreachable):
        self.state_row = np.concatenate((np.array([0]), reachable, unreachable), axis=0)  # rbind

def check_sum(array_to_check, val):
    """
    check to see if each element in the array is 1
    :param array_to_check:
    :return:
    """
    for each_ele in array_to_check:
        assert(each_ele == val)
    print("array elements are all %d" %val)


def create_transistion_matrix(matrix_probabilities, mdp_domain):
    """
    The number of actions, the number of states, the number of states
    num_actions x num_states x num_states
    """
    # the initial state, the array of valid moves, the trailing zeros
    r_good_side = mdp_domain.state_row

    # transitions zeros
    transistions = [mdp_domain.state_row]

    # create the state transition matrix
    for i in range(len(mdp_domain.state_row) - 1):
        r_good_side = np.roll(r_good_side, 1)
        transistions = np.concatenate((transistions, [r_good_side]), axis=0)

    # only take the upper right part of the matrix and multiple by the probability of transistioning
    matrix_probabilities[1] = np.triu(transistions)  # upper triangle matirx

    return matrix_probabilities


def make_probability(matrix_probabilities, probability_dice, n_states):
    """
    make the transistion probability matrix into a probability matrix
    :param matrix_probabilities:
    :param probability_dice:
    :param n_states:
    :return:
    """
    matrix_probabilities[1] = matrix_probabilities[1] * probability_dice
    # the probability of ending up with the cash
    prob_quit = 1 - np.sum(matrix_probabilities[1, :n_states, :n_states - 1], axis=1).reshape(-1, 1)  # last column

    # add onto the end of the state transistion
    matrix_probabilities[1] = np.concatenate((matrix_probabilities[1, :n_states, :n_states - 1], prob_quit), axis=1)  # cbind

    check_sum(np.sum(matrix_probabilities[1], axis=1), 1)  # test column sum
    return matrix_probabilities

def make_reward(matrix, n_states):
    """
    make the reward matrix
    :param matrix:
    :param n_states:
    :return:
    """
    reward_matrix_quit = - np.array(range(0, n_states)).reshape(-1, 1)  # convert vector to n X 1 matrix
    matrix[1] = np.concatenate((matrix[1, :n_states, :n_states - 1], reward_matrix_quit), axis=1)  # cbind
    return matrix

def main():
    # the number of sides of the die
    n_sides=6

    # the number of rolls of the die
    n_runs = 2

    # the number of actions
    n_actions = 2

    # beginning and ending states
    n_initial_terminal_states = 2

    # the number of total states
    n_states = n_runs * n_sides + n_initial_terminal_states  # from 0 to 2N, plus quit

    # the boolean mask to indicate which states you will loose money on
    isBadSide = np.array([1, 1, 1, 0, 0, 0])
    isGoodSide = [not i for i in isBadSide]

    # the array which contains the values of the die
    die = np.arange(1, n_sides + 1)  # [1, 2, 3, 4, 5, 6]

    # the total earnings given a die roll
    earnings = die * isGoodSide  # [0, 0, 0, 4, 5, 6]

    # Calculate probability for Input:
    probability_dice = 1.0 / n_sides

    # crate the domain class
    mdp_domain = MDP_Domain(n_sides, n_runs, n_actions, n_initial_terminal_states)

    transistion_probabilities = np.zeros((mdp_domain.n_actions, mdp_domain.n_states, mdp_domain.n_states))

    # the probability that you will not roll the dice, will transition from the same state
    np.fill_diagonal(transistion_probabilities[0], 1)

    # the number of zeros trailing
    unreachable_states = np.array([0]).repeat((n_runs - 1) * n_sides + 1)

    mdp_domain.create_state_transistions(isGoodSide, unreachable_states)

    # Create probability array==========================
    transistion_probabilities = create_transistion_matrix(transistion_probabilities, mdp_domain)
    transistion_probabilities = make_probability(transistion_probabilities, probability_dice, mdp_domain.n_states)


    # Create rewards array==========================
    reward_matrix = np.zeros((n_actions, n_states, n_states))
    # if leave
    reward_matrix[0] = np.zeros((n_states, n_states))
    mdp_domain.create_state_transistions(earnings, unreachable_states)
    reward_matrix = create_transistion_matrix(reward_matrix, mdp_domain)
    reward_matrix = make_reward(reward_matrix, n_states)

    vi = mdptoolbox.mdp.ValueIteration(transistion_probabilities, reward_matrix, .99999)
    vi.run()

    optimal_policy = vi.policy
    expected_values = vi.V

    print(optimal_policy)
    print(expected_values)

main()