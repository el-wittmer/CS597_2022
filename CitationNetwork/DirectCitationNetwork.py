"""
El Wittmer
06.26.2022

Environment: Requires installation of pandas, mathplotlib, igraph, and py3cairo

"""

# Import pandas, read in csv file containing citation data and drop any rows that contain null values

import pandas as pd
# read in citation data
df = pd.read_csv(f'histone_export.csv')
# drop any rows that contain Null values
df.dropna(
    axis=0,
    how='any',
    thresh=None,
    subset=None,
    inplace=True
)

# Get an edge, node count

node_set = set()
for i in range(len(df)):
    node_set.add(df['citing'].iloc[i])
    node_set.add(df['cited'].iloc[i])
print(len(df), len(node_set))

"""
To filter data, need to organize citations by the number of times a paper has been cited
Keep only the cited papers that fulfill a set criteria (I kept those cited > 500 times)
"""

# only need the citing/cited columns
df_count = df[['citing', 'cited']]
# and a count of the number of times each cited paper is cited
df_count = df_count.groupby('cited').count()
# this returns one column with two values in it, we need to fix that
# theres probably an easier way than exporting and re-importing
df_count.to_csv('cited_count.tsv', sep='\t', header=True)
df_count = pd.read_csv('cited_count.tsv', sep='\t', header=0)
df_count = df_count.rename(columns={'citing': 'count'})
df_count = df_count.sort_values('count', ascending=False)
df_count = df_count.iloc[:21] # papers w/ > 500 citations

"""
For each paper kept, need to get all the papers that cited that paper
"""

# get the right edges based on the cited nodes kept
filter_cited = df_count['cited'].to_list()
filtered_edges = []
for i in range(len(df)):
    if df['cited'].iloc[i] in filter_cited:
        filtered_edges += [(df['citing'].iloc[i], df['cited'].iloc[i])]
filter_df = pd.DataFrame(filtered_edges, columns=['citing', 'cited'])
filter_df = filter_df.drop_duplicates()

# Updated edge, node count

filter_node_set = set()
for i in range(len(filter_df)):
    filter_node_set.add(filter_df['citing'].iloc[i])
    filter_node_set.add(filter_df['cited'].iloc[i])
print(len(filter_df), len(filter_node_set))

"""
Each node in the filtered dataset needs to be assigned an integer id to be compliant 
with Leiden algorithm input file requirements
"""

# for each node kept, assign an integer index starting at 0

selected_columns = filter_df
temp = selected_columns.copy()
temp = temp.stack().reset_index()
node_list = temp[0].unique()

node_index = {}
node_count = len(node_list)
for i in range(node_count):
    node_index[node_list[i]] = i
    

# For each of the rows in the filtered data set, convert each value to its integer id

edge_list = []
# replace each doi with its integer index
for j in range(len(filter_df)):
    edge = (filter_df['citing'].iloc[j], filter_df['cited'].iloc[j])
    edge_list += [(node_index.get(edge[0]), node_index.get(edge[1]))]
filter_network = pd.DataFrame(edge_list)

# Write filtered network to file

filter_network.to_csv('filter_network.tsv', sep='\t',index=False, header=False)
