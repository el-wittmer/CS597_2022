import pandas as pd


# get nodes and edges from data files (hard-coded)
edges = pd.read_csv("~/Downloads/Leng_2021_Edges.csv", header=0)
nodes = pd.read_csv("~/Downloads/Leng_2022_Nodes.csv", header=0)

# remove publications not written in English
nodes = nodes.drop(nodes[nodes.Citation_context == "Foreign"].index)

for year in range(1964, 1985):

  # get a list of all the nodes remaining in the dataset
  filter_nodes = []
  for j in range(len(nodes)):
      filter_nodes += [nodes["Id"].iloc[j]]

  # if both the citing and cited nodes are in the list of nodes kept, add them to a list
  edges_list = []
  for i in range(len(edges)):
      if edges["Source"].iloc[i] in filter_nodes and edges["Target"].iloc[i] in filter_nodes:
              edges_list += [(edges["Source"].iloc[i], edges["Target"].iloc[i])]

  # make a new data frame of the network           
  network_df = pd.DataFrame(edges_list, columns=["Source", "Target"])
  
  # for each year, get a new tsv file
  network_df.to_csv(f"Paul_network_{year}.tsv", sep="\t", index=False, header=False)
