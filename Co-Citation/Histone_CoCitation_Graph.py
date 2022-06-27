"""
El Wittmer 
6.11.2022

This function takes an integer as a parameter and creates a graph that includes each co-citation pair 
with a frequency count equal than or greater to that number.

"""

import networkx as nx
import matplotlib.pyplot as plt

def graph_co_citation(int):

    G = nx.Graph()

    keys = count_dict.keys()
    edge_list = [('Item 1', 'Item 2')]
    # for each co-citation pair
    for j in keys:
    # if the number of co-citation occurances is greater or equal to (int)
        if count_dict.get(j) >= int:
            edge = j.split()
            # get both items in the pair and add to a list of tuples
            edge_list.append((edge[0], edge[1]))
    # delete the header
    del edge_list[0]

    # each item in the list of edges is a node
    # does this add multiple nodes of the same doi? Investigate
    for i in edge_list:
        G.add_node(edge_list[0])
        G.add_node(edge_list[1])

    G.add_edges_from(edge_list)

    nx.draw(G)
    plt.draw()
