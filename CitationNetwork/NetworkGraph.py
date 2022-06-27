"""
El Wittmer
06.26.2022

Requires installation of igraph, py3cairo to run
Input file is the output of the Leiden algorithm, a tsv file in [node cluster_id] format
"""

import igraph as ig
from igraph import Graph

"""
Read in clustering document, get the desired clusters and the nodes in them
"""
leiden_04 = pd.read_csv(f'leiden_04.tsv', sep='\t', header=None)
leiden_04 = leiden_04.rename(columns={0: 'node', 1: 'cluster_id'})
leiden_04 = leiden_04.sort_values('cluster_id')
leiden_04 = leiden_04.iloc[:250]
node_list = leiden_04['node'].tolist()

"""
Without adding any new nodes, build edges between nodes in the cluster if they exist in original network
"""
cluster_edges = []
for i in range(len(filter_network)):
    if filter_network[0].iloc[i] in node_list and filter_network[1].iloc[i] in node_list:
        cluster_edges += [(filter_network[0].iloc[i], filter_network[1].iloc[i])]
cluster_edges = pd.DataFrame(cluster_edges)

g = Graph.DataFrame(cluster_edges, directed=True)
ig.plot(g)
