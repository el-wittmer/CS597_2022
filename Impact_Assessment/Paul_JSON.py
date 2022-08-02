import pandas as pd
import JSON as json
import unicodedata

# read in data files
edges = pd.read_csv("~/Downloads/Leng_2021_Edges.csv", header=0)
nodes = pd.read_csv("~/Downloads/Leng_2022_Nodes.csv", header=0)

# drop publications not written in English and reset the index
nodes = nodes.drop(nodes[nodes.Citation_context == "Foreign"].index)
nodes = nodes.reset_index()
nodes = nodes.rename(columns={"Label": "First_Author"})

# standardize formatting in cluster columns
for j in range(len(nodes)):
    if str(nodes["Cluster"].iloc[j]) == "nan":
        nodes.iat[j, -2] = 9
        nodes.iat[j, -1] = "Undefined"
    else:
        topic = unicodedata.normalize("NFKD", nodes.iat[j, -1])
        nodes.iat[j, -1] = topic
       
# values can be adjusted accordingly      
start_year = 1963 # non-inclusive
end_year = 1984 # inclusive

json_nodes = []
filter_nodes = []
for i in range(len(nodes)):
    filter_year = int(nodes["Publication_Year"].iloc[i])
    if filter_year <= end_year and filter_year > start_year:
        filter_nodes += [nodes["Id"].iloc[i]]
        json_nodes += [{"Id": str(nodes["Id"].iloc[i]), "First_Author" : nodes["First_Author"].iloc[i], 
                "Title" : nodes["Title"].iloc[i], "Publication_Year" : str(nodes["Publication_Year"].iloc[i]), 
                "Publication_Source": nodes["Publication"].iloc[i], "WoS_ID" : nodes["WoS_ID"].iloc[i], "Cluster" : nodes["Cluster"].iloc[i],
                "Topic": nodes['Cluster_Name'].iloc[i]}]

filter_edges = []
for j in range(len(edges)):
    # filter out nodes based on year
    if edges["Source"].iloc[j] in filter_nodes and edges['Target'].iloc[j] in filter_nodes: 
        filter_edges += [{"source": str(edges["Source"].iloc[j]), "target" : str(edges["Target"].iloc[j])}]

json_data = {"nodes" : json_nodes, "links" : filter_edges}

with open(f"Paul_{start_year}-{end_year}.json", "w") as outfile:
    json.dump(json_data, outfile)
