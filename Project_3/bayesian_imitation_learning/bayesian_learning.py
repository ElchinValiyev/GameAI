import kmeans
import numpy as np
from sklearn.preprocessing import normalize
import helper as hp


def find_activity_vectors(data_points):
    activity_vectors = []
    for i in range(len(data_points) - 1):
        activity = data_points[i + 1] - data_points[i]
        activity_vectors.append(activity.tolist())
    return activity_vectors


def find_probability_matrix(state_indices, action_indices, s_centers, a_centers):
    matrix = np.zeros((len(s_centers), len(a_centers)))
    for i in range(len(action_indices)):
        s_i = state_indices[i]
        r_j = action_indices[i]
        matrix[s_i][r_j] += 1
    probability_matrix = matrix / np.sum(matrix)
    # probability_matrix = normalize(state_action_probabilities,norm='l1')
    return probability_matrix


def generate_path(probability_matrix, state_prototypes, action_prototypes, iterations):
    path = []
    state_index = np.random.randint(len(state_prototypes))
    current_position = state_prototypes[state_index]
    # path.append(current_position)
    for i in range(iterations):
        path.append(current_position)
        best_action_index = np.argmax(probability_matrix[state_index])
        best_action = action_prototypes[best_action_index]
        current_position = current_position + best_action
        dist = [kmeans.distance(current_position, k) for k in state_prototypes]
        min_index, = np.where(dist == np.min(dist))
        state_index = min_index[0]
    return path


def run_bayesian_learning(points_filename, som_centers_filename, activity_centers_num, path_iterations_num):
    data_points = hp.read_points(points_filename)
    activity_vectors = find_activity_vectors(data_points)

    activity_indices, prototypical_activities = kmeans.kmeans(activity_centers_num, activity_vectors)
    prototypical_states = hp.read_points(som_centers_filename)
    # e-step assigns each state to the closest prototypical state
    state_indices = kmeans.e_step(prototypical_states, data_points)
    probability_matrix = find_probability_matrix(state_indices, activity_indices, prototypical_states,
                                                 prototypical_activities)
    path = np.array(
        generate_path(probability_matrix, prototypical_states, prototypical_activities, path_iterations_num))
    return path

# path = run_bayesian_learning()
# hp.plot_points(path[:, 0], path[:, 1], path[:, 2],"generated path")
