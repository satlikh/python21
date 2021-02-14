# Import required modules
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from matplotlib.collections import LineCollection
from scipy import spatial
import time

# Task 1 ==================================================
def read_coordinate_file(filename_fun):
    """
    Reads the given coordinate text file and parses the results into an array of coordinates.
    Parameters.

    :param filename_fun: The file location of the .txt file which contains coordinates expressed in the format:
        {a, b} where 'a'is the latitude and 'b' is the longitude (in degrees).
    :type filename_fun: str

    :return: A 2D numpy array in the shape of [n_city × 2] which contains the coordinates of cities in xy-format.
        n_city is the number of cities in the main file.
    :rtype: coord_list: 2D NumPy array
    """
    with open(filename_fun, 'r') as file:
        x = []
        y = []
        r = 1
        for lines in file:
            coords = (lines.strip('{}\n'))
            a_temp, b_temp = coords.split(sep=',')
            a, b = float(a_temp), float(b_temp)
            x.append(r * (math.pi * b) / 180)
            y.append(r * math.log(math.tan(math.pi / 4 + (math.pi * a) / 360)))

    return np.array([x, y]).T


# Task 3 =================================================
def construct_graph_connections(coord_list_fun, radius_fun):
    """
    Computes all the connections between all the points in `coord_list_fun` that are within the given
    `radius_fun`.It returns the indices of cities and their corresponding distances in another 2D numpy array.

    :param coord_list_fun: A 2D numpy array in the shape of [n_city × 2] which contains the coordinates of cities
        in xy-format.
    :type coord_list_fun: 2D numpy array

    :param radius_fun: The maximum acceptable distance between two cities to be connected.
    :type radius_fun: float


    :return: Indices of cities which can be connected. The indices are according the city orders in `coord_list`
        array.
    :rtype: indices_fun: 2D numpy array

    :return: The corresponding distances of cities in the `indices_fun`.
    :rtype: distance_fun: 2D numpy array
    """
    indices_fun, distance_fun = [], []
    if coord_list_fun.shape[0] == 2:  # re-orders the list tp {x, y} for easier looping
        coord_list_fun = np.transpose(coord_list_fun)

    for i, value_i in enumerate(coord_list_fun):
        city_distance = np.linalg.norm(coord_list_fun[(i + 1):] - value_i, axis=1)
        for j, dist in enumerate(city_distance, (i + 1)):
            if dist < radius_fun:
                indices_fun.append([i, j])
                distance_fun.append(dist)

                indices_fun.append([j, i])  # to create both pathways
                distance_fun.append(dist)
    return np.array(indices_fun, dtype=int), np.array(distance_fun)


# Task 4 =================================================
def construct_graph(indices, distance, N):
    """
    Constructs a sparse graph using 'scipy' compresses sparse row matrix (csr_matrix in scipy.sparse).

    :param indices: Indices of connected nodes (cities) in a 2d numpy array according their order in `coord_list`.
    :type indices: 2D numpy array

    :param distance: The corresponding distances of connected nodes (cities) in the indices.
    :type distance: 2D numpy array

    :param N: Number of nodes (cities) in the graph.
    :type N: int


    :return: A 2D csr-matrix which represents the graph of connected cities.
    :rtype: graph: scipy csr sparse matrix
    """
    # Hint:
    # csr_matrix((data, (row_ind, col_ind)), [shape=(M, N)])
    data = np.array(distance)
    data = data.reshape((-1,))
    row = indices[:, 0]
    col = indices[:, 1]

    graph = csr_matrix((data, (row, col)), shape=(N, N))
    return graph


# Task 6 =================================================
def find_shortest_paths(graph, start_node):  # using dijkstra
    """
    Uses Dijkstra algorithm using Fibonacci Heaps to find the shortest path from a start point to all other
    points.

    :param graph: The N x N array of non-negative distances representing the input graph.
    :type graph: array, matrix, or sparse matrix, 2 dimensions

    :param start_node: The start point to compute the shortest paths
    :type start_node: array_like or int


    :return: The matrix of distances between graph nodes. dist_matrix has shape (n_indices, n_nodes) and
        dist_matrix[i, j] gives the shortest distance from point i to point j along the graph.
    :rtype: dist_matrix: 2D numpy array

    :return: Returned only if return_predecessors == True. The matrix of predecessors, which can be used to
        reconstruct the shortest paths. Row i of the predecessor matrix contains information on the shortest
        paths from point i: each entry predecessors[i, j] gives the index of the previous node in the path
        from point i to point j. If no path exists between point i and j, then predecessors[i, j] = -9999
    :rtype: predecessors: 2D numpy array
    """
    [dist_matrix, predecessors] = dijkstra(csgraph=graph,
                                           directed=True,
                                           indices=start_node,
                                           return_predecessors=True)
    return dist_matrix, predecessors


# Task 7 =================================================
def compute_path(predecessors_matrix, start_node, end_node):
    """
    Computes the shortest path from `start_node` to `end_node` given `predecessors_matrix`.

    :param predecessors_matrix: The matrix of predecessors, which can be used to reconstruct the shortest paths.
        Row i of the predecessor matrix contains information on the shortest paths from point i: each entry
        predecessors[i, j] gives the index of the previous node in the path from point i to point j. If no path
        exists between point i and j, then predecessors[i, j] = -9999
    :type predecessors_matrix: 2D numpy array (n_cities x 1)

    :param start_node: Starting node of the path.
    :type start_node: int

    :param end_node: End node of the path
    :type end_node: int


    :return: List of nodes from start_node till end_node. If there was not any path from start_node till
        end_node, an empty list would be returned with a message.
    :rtype: path: list
    """
    previous_node = end_node
    path = [end_node]

    while previous_node != start_node:
        if predecessors_matrix[previous_node] != -9999:
            path.append(predecessors_matrix[previous_node])
            previous_node = predecessors_matrix[previous_node]
        else:
            path = []
            print('There is no path from {} to {}'.format(start_node, previous_node))
            return path

    return path[::-1]


# Task 2, 5 & 8 =================================================
def plot_points(coord_list, indices, path):
    """
    Plots the data points, their connecting lines and given `path`.

    :param coord_list : A 2D numpy array in the shape of [n_city × 2] which contains the coordinates of
        cities in xy-format. n_city is the number of cities in the main file.
    :type coord_list: 2D Numpy array

    :param indices: dices of cities can be connected. The indices are according the city orders in
        `coord_list` array.
    :type indices: 2D numpy array

    :param path: A sequence of nodes (cities) in a list to represent a path from first item on the list to the
        end item.
    :type path: list

    :return: Plots the given city coordinates on a plain with small filled red circles, their connections and
        the given path.
    """
    fig_size = (9, 6)
    marker_size = 5
    if coord_list.shape[0] == 7:
        fig_size = (9, 6)
        marker_size = 7
    elif coord_list.shape[0] == 850:
        fig_size = (12, 8)
        marker_size = 5
    elif coord_list.shape[0] == 12060:
        fig_size = (15, 15)
        marker_size = 2

    fig = plt.figure(figsize=fig_size)
    plt.plot(coord_list[:, 0], coord_list[:, 1], 'or',
             markersize=marker_size,
             label='City')

    plt.title('City Plots & their connections', fontweight='bold', fontsize=17)
    ax = plt.gca()

    ax.set_xlabel('X - Coordinate', fontweight='bold', fontsize=12)
    ax.set_ylabel('Y - Coordinate', fontweight='bold', fontsize=12)
    plt.axis('equal')
    # plt.legend(loc='best');

    # ====================================================================
    x_coord, y_coord = coord_list[:, 0], coord_list[:, 1]
    segments = np.zeros((len(indices), 2, 2))
    x_segments = x_coord[indices]
    y_segments = y_coord[indices]
    segments[:, :, 0], segments[:, :, 1] = x_segments, y_segments

    line_segments = LineCollection(segments,
                                   linewidths=1.0,
                                   colors='0.5',
                                   label='Connection')
    ax.add_collection(line_segments)
    # ====================================================================
    # Plot path
    if len(path) > 0:
        path_length = len(path)  # number of nodes on the path
        path_lines = []
        for i in range(path_length - 1):
            path_lines.append((coord_list[path[i], :], coord_list[path[i + 1], :]))

        path_line_segments = LineCollection(path_lines,
                                            linewidths=4,
                                            colors='b',
                                            label='Path')
        ax.add_collection(path_line_segments)
    # ====================================================================
    plt.legend(loc='best')
    plt.show()


# Task 10 =================================================
def construct_fast_graph_connections(coord_list, radius):
    """
    Computes all the connections between all the points in `coord_list_fun` that are within the given
    `radius_fun`.It returns the indices of cities and their corresponding distances in another 2D numpy array.
    It uses cKDTree object and query_ball_point() function to compute the connections.

    :param coord_list: A 2D numpy array in the shape of [n_city × 2] which contains the coordinates of cities
        in xy-format.
    :type coord_list: 2D numpy array

    :param radius: The maximum acceptable distance between two cities to be connected.
    :type radius: float


    :return: Indices of cities which can be connected. The indices are according the city orders in `coord_list`
        array.
    :rtype: indices: 2D numpy array

    :return: The corresponding distances of cities in the `indices`.
    :rtype: distance: 2D numpy array
    """
    indices = []
    distance = []
    graph_tree = spatial.cKDTree(coord_list)
    connections = graph_tree.query_ball_point(coord_list, radius)  # The cities in vicinity of redius
    for i, i_connection in enumerate(connections):  # i_connectoin: connected cities to city i
        for j in i_connection:  # j is the index of connected city to city i in coord_list
            if i != j:
                indices.append([i, j])
                dist_ij = np.linalg.norm(coord_list[i, :] - coord_list[j, :])
                distance.append(dist_ij)

    return np.array(indices, dtype=int), np.array(distance)


# Task 9 =================================================
# (filename, radius, start_node, end_node) = ('SampleCoordinates.txt', 0.08, 0, 5)
# (filename, radius, start_node, end_node) = ('HungaryCities.txt', 0.005, 311, 702)
(filename, radius, start_node, end_node) = ('GermanyCities.txt', 0.0025, 1573, 10584)

start = time.time()
coord_list = read_coordinate_file(filename)
end = time.time()
task1_time = end - start

start = time.time()
indices, distance = construct_graph_connections(coord_list, radius)
end = time.time()
t_construct_graph_connections = end-start

start = time.time()
graph = construct_graph(indices, distance, coord_list.shape[0])
end = time.time()
t_construct_graph = end-start

start = time.time()
dist_matrix, predecessors = find_shortest_paths(graph, start_node)
path = compute_path(predecessors, start_node, end_node)
end = time.time()
t_6_7 = end-start

start = time.time()
plot_points(coord_list, indices, path)
end = time.time()
t_plot_points = end-start

start = time.time()
ind, dist = construct_fast_graph_connections(coord_list, radius)
end = time.time()
t_construct_fast_graph_connections = end - start


start = time.time()
coord_list = read_coordinate_file(filename)
indices, distance = construct_fast_graph_connections(coord_list, radius)
graph = construct_graph(indices, distance, coord_list.shape[0])
dist_matrix, predecessors = find_shortest_paths(graph, start_node)
path = compute_path(predecessors, start_node, end_node)
end = time.time()
t_total = end-start

t_str_read_coordinate_file = '{:.3f}'.format(task1_time)
t_str_construct_graph_connections = '{:.3f}'.format(t_construct_graph_connections)
t_str_construct_graph = '{:.3f}'.format(t_construct_graph)
t_str_6_7 = '{:.3f}'.format(t_6_7)
t_str_plot_points = '{:.3f}'.format(t_plot_points)
t_str_construct_fast_graph_connections = '{:.3f}'.format(t_construct_fast_graph_connections)
t_str_total = '{:.3f}'.format(t_total)

# from tabletext import to_text
a = [["function ", "reference time (s)", "time (s)"],
     ["read_coordinate_file", "0.030", t_str_read_coordinate_file],
     ["construct_graph_connections", "70.000", t_str_construct_graph_connections],
     ["construct_graph", "0.002", t_str_construct_graph],
     ["Task 6+7", "0.007", t_str_6_7],
     ["plot_points (from task 8, excluding plt.show)", "2.000", t_str_plot_points],
     ["construct_fast_graph_connections", "0.300", t_str_construct_fast_graph_connections],
     ["Running the entire program using the fast version, excluding plotting", "1.000", t_str_total]]
# print(to_text(a, header=True, header_corners="╒╤╕╞╪╡"))


# Task: Final Part =================================================
def plot_and_compute_path(filename, radius, start_node, end_node):
    """
    Reads the file and coordinates of the cities in it. Then it constructs the graph of cities and finds the
    shortest path between two given points by plotting and computing the path and their distance.

    :param filename: The file location of the .txt file which contains coordinates expressed in the format:
        {a, b} where 'a'is the latitude and 'b' is the longitude (in degrees).
    :type filename: str

    :param radius: The maximum acceptable distance between two cities to be connected.
    :type radius: float

    :param start_node: Starting node of the path.
    :type start_node: int

    :param end_node: End node of the path.
    :type end_note: int
    """
    filename_without_extension = filename[0:-4]

    coord_list = read_coordinate_file(filename)
    indices, distance = construct_fast_graph_connections(coord_list, radius)
    graph = construct_graph(indices, distance, coord_list.shape[0])
    dist_matrix, predecessors = find_shortest_paths(graph, start_node)
    path = compute_path(predecessors, start_node, end_node)
    plot_points(coord_list, indices, path)
    plt.savefig('{}.png'.format(filename_without_extension))

    print("For {}:".format(filename[0:-4]))
    print("Shortest path from {p1} to {p2} is:\n{path}\n".format(p1=start_node, p2=end_node, path=path))
    print("The shortest distance between {p1} and {p2} is:\n{dist}\n\n".format(p1=start_node,
                                                                               p2=end_node,
                                                                               dist=dist_matrix[end_node]))

# Task: Final Part =================================================
test_set = [['SampleCoordinates.txt', 0.08, 0, 5],
            ['HungaryCities.txt', 0.005, 311, 702],
            ['GermanyCities.txt', 0.0025, 1573, 10584]]

for filename, radius, start_node, end_node in test_set:
    plot_and_compute_path(filename, radius, start_node, end_node)

