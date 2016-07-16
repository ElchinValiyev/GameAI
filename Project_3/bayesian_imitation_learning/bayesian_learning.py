import kmeans
import numpy as np
from sklearn.preprocessing import normalize
import helper as hp
import random


# activity vectors as differences between subsequent states
def find_activity_vectors(data_points):
    activity_vectors = []
    for i in range(len(data_points) - 1):
        activity = data_points[i + 1] - data_points[i]
        activity_vectors.append(activity.tolist())
    return activity_vectors


# state_indices - vector of data length where each element is index of closest prototypical state
# action_indices - vector of data length where each element is index of closest prototypical activity
def find_probability_matrix(state_indices, action_indices, s_centers, a_centers):
    matrix = np.zeros((len(s_centers), len(a_centers)))
    for i in range(len(action_indices)):  # sum up activity prototypes and state prototypes occurring together
        s_i = state_indices[i]
        r_j = action_indices[i]
        matrix[s_i][r_j] += 1
    probability_matrix = matrix / np.sum(matrix)  # normalize - divide by sum of all elements
    # probability_matrix = normalize(matrix,norm='l1')
    return probability_matrix


def generate_path(probability_matrix, state_prototypes, action_prototypes, state_indices, iterations):
    state_index = random.sample(state_indices, 1)[0]  # select random point
    path = []
    current_position = state_prototypes[state_index]  # choose closest state prototype
    for i in range(iterations):
        path.append(current_position)
        # following should not be the case but who knows what is going on with 2nd map
        if np.sum(probability_matrix[state_index]) == 0:
            best_action_index = np.argmax((probability_matrix[state_index]))
        else:
            # choose best action using matrix of joint probabilities
            best_action_index = np.argmax((probability_matrix[state_index] / np.sum(probability_matrix[state_index])))
        best_action = action_prototypes[best_action_index]
        current_position = current_position + best_action
        dist = [kmeans.distance(current_position, k) for k in state_prototypes]
        min_index, = np.where(dist == np.min(dist))  # choose closest prototype
        state_index = min_index[0]
    return path


def run_bayesian_learning(points_filename, som_centers_filename, activity_centers_num, path_iterations_num):
    data_points = hp.read_points(points_filename)
    activity_vectors = np.array(find_activity_vectors(data_points))
    # prototypical activities - centers of clusters of activities
    # prototypical_activities - vector of data length where each element is index of closest prototypical activity
    activity_indices, prototypical_activities = kmeans.kmeans(activity_centers_num, activity_vectors)
    prototypical_states = hp.read_points(som_centers_filename)
    # e-step assigns each state to the closest prototypical state
    # prototypical_states - vector of data length where each element is index of closest prototypical state
    state_indices = kmeans.e_step(prototypical_states, data_points)
    probability_matrix = find_probability_matrix(state_indices, activity_indices, prototypical_states,
                                                 prototypical_activities)
    path = np.array(
        generate_path(probability_matrix, prototypical_states, prototypical_activities, state_indices,
                      path_iterations_num))
    return path
