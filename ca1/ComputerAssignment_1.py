import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
import time


def read_coordinate_file(filename_fun):
    """Reads the given coordinate text file and parses the results into an array of coordinates.
    Parameters
    ----------
    filename_fun : str
        The file location of the .txt file which contain coordinates expressed in the format: {a, b} where a
        is the latitude and b is the longitude (in degrees).

    Returns
    -------
    2D NumPy array
        A 2D numpy array in the shape of [2 × n_city] which contains the coordinates of cities in xy-format.
        n_city is the number of cities in the main file.
    """
    file = open(filename_fun, 'r')
    line = file.readline()
    i = 0
    x, y = [], []
    r = 1
    while line:
        coord_lat = line.strip('{}\n')
        a_temp, b_temp = coord_lat.split(sep=',')
        a, b = float(a_temp), float(b_temp)
        x.append(r * (np.pi * b) / 180)
        y.append(r * np.log(np.tan(np.pi / 4 + (np.pi * a) / 360)))  # conversion to coordinates
        line = file.readline()
        i += 1
    file.close()
    return np.transpose([x, y])


"""Question 3"""


def construct_graph_connections(coord_list_fun, radius_fun):
    indices_fun, distance_fun = [], []
    for i, value_i in enumerate(coord_list_fun):
        city_distance = np.linalg.norm(coord_list_fun[(i+1):] - value_i, axis=1)
        for j, dist in enumerate(city_distance, (i+1)):
            if dist < radius_fun:
                indices_fun.append([i, j])
                distance_fun.append(dist)
                indices_fun.append([j, i])  # to create both pathways
                distance_fun.append(dist)
    return np.array(indices_fun), np.array(distance_fun)


"""Question 4"""


def construct_graph(indices, distance, N):

    # csr_matrix((data, (row_ind, col_ind)), [shape=(M, N)])
    data = np.array(distance)
    data = data.reshape((-1,))
    row = np.array(indices[:, 0])
    col = np.array(indices[:, 1])

    # print(data.shape, row.shape, col.shape)

    csr_distance = csr_matrix((data, (row, col)), shape=(N, N))
    return csr_distance


"""Question 6"""


def find_shortest_paths(graph, start):  # using dijkstra
    dist_matrix, predecessors = dijkstra(csgraph=graph,
                                         directed=True,
                                         indices=start,
                                         return_predecessors=True)
    return dist_matrix, predecessors


"""Question 7"""


def compute_path(predecessor_matrix, start_node, end_node):
    j = end_node
    path = []
    path.append(j)

    # Check the shape of predecessors array
    n_city = predecessor_matrix.shape[0]

    if (n_city,) == np.shape(predecessor_matrix):  # if so; it is an 1D array with shape: (n_city, n_city)
        while j != start_node:
            if predecessor_matrix[j] != -9999:
                path.append(predecessor_matrix[j])
                j = predecessor_matrix[j]
            else:
                path = []
                print('\n', "There is no path from/to determined cities!", '\n')
                return path
            # End of if
        # End of while loop
    else:

        while j != start_node:
            if predecessor_matrix[start_node, j] != -9999:
                path.append(predecessor_matrix[start_node, j])
                j = predecessor_matrix[start_node, j]
            else:
                path = []
                print('\n', "There is no path from/to determined cities!", '\n')
                return path
            # End of if
        # End of while loop

    # print("path=",path[::-1]) # [::-1] to reverse the path
    return path[::-1]


"""Question 2,5 and 8"""


def plot_points(coord_list, indices, path):

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
    # Plotting connections
    lines = []
    for p1, p2 in indices:
        line = [(coord_list[int(p1), 0], coord_list[int(p1), 1])]
        line.append((coord_list[int(p2), 0], coord_list[int(p2), 1]))
        lines.append(line)

    line_segments = LineCollection(lines,
                                   linewidths=1.0,
                                   colors='0.5',
                                   label='Connection')
    # ax = fig.gca()
    ax.add_collection(line_segments)
    # ====================================================================
    # Plotting path
    if path != None:
        shortest_path_length = len(path)  # number of nodes on shortest path
        shortest_path_lines = []
        for i in range(shortest_path_length - 1):
            shortest_path_lines.append((coord_list[path[i], :], coord_list[path[i + 1], :]))

        shortest_path_line_segments = LineCollection(shortest_path_lines,
                                                     linewidths=4,
                                                     colors='b',
                                                     label='Path')
        ax.add_collection(shortest_path_line_segments)
    # ====================================================================
    # Annotate each city based in their order
    # n = np.arange(coord_list.shape[0])
    # for i,txt in enumerate(n):
    #    ax.annotate(txt, (coord_list[i,0], coord_list[i,1]),size=13)

    plt.legend(loc='best')
    # plt.show()


"""Question 9"""
# filename = 'SampleCoordinates.txt'
# filename = 'HungaryCities.txt'
filename = 'GermanyCities.txt'

read_start = time.time()
coord_list = read_coordinate_file(filename)
read_stop = time.time()
print('reading time:', read_stop - read_start, 'seconds')

var = {'SampleCoordinates.txt': dict(radius=0.08, start_city=0, end_city=5),
       'HungaryCities.txt': dict(radius=0.005, start_city=311, end_city=702),
       'GermanyCities.txt': dict(radius=0.0025, start_city=1573, end_city=10584)}
city = var[filename]  # retrieves the variable for the radius, start- and end-city for the files

const_con_start = time.time()
indices, distance = construct_graph_connections(coord_list, city['radius'])
const_con_stop = time.time()
print('Constructing connection points time:', const_con_stop - const_con_start, 'seconds')

n_city = coord_list.shape[0]

const_graph_start = time.time()
city_graph = construct_graph(indices, distance, n_city)
const_graph_stop = time.time()
print('Construction graph time:', const_graph_stop - const_graph_start,' seconds')

Q67_start = time.time()
dist_matrix, predecessors = find_shortest_paths(city_graph, start=city['start_city'])
shortest_path = compute_path(predecessors, city['start_city'], city['end_city'])
Q67_stop = time.time()
print('Question 6 & 7 time:', Q67_stop - Q67_start, ' seconds')

plot_start = time.time()
plot_points(coord_list, indices, shortest_path)
plot_stop = time.time()
print('Plotting time:', plot_stop - plot_start, ' seconds')
plt.show()
