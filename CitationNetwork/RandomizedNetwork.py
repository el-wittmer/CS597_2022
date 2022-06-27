"""
Import pandas, read in csv file containing citation data and drop any rows that contain null values
"""

import pandas as pd
import random
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

"""
To filter data, need to organize citations by the number of times a paper has been cited
Keep only the cited papers that fulfill a set criteria (I kept those cited > 500 times)
"""

# only need the citing/cited columns
df_count = df[['citing', 'cited', 'cited_pub_year']]
# and a count of the number of times each cited paper is cited
df_count = df_count.groupby('cited').count()
# this returns one column with two values in it, we need to fix that
df_count.to_csv('cited_count.tsv', sep='\t', header=True)
df_count = pd.read_csv('cited_count.tsv', sep='\t', header=0)
df_count = df_count.rename(columns={'citing': 'count'})
df_count = df_count.sort_values('count', ascending=False)
df_count = df_count.iloc[:21] # papers w/ > 1000 citations

"""
For each paper kept, need to get all the papers that cited that paper
"""

# get the right edges based on the cited nodes kept
filter_cited = df_count['cited'].to_list()
filtered_edges = []
for i in range(len(df)):
    if df['cited'].iloc[i] in filter_cited:
        filtered_edges += [(df['citing'].iloc[i], df['cited'].iloc[i], df['cited_pub_year'].iloc[i])]
filter_df = pd.DataFrame(filtered_edges, columns=['citing', 'cited', 'cited_pub_year'])
filter_df = filter_df.drop_duplicates()

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
    
"""
Get a dictionary of the form {year: [cited1, cited2]}
"""
cited_year_dict = {}

for i in range(len(filter_df)):
    cited_year = int(filter_df['cited_pub_year'].iloc[i])
    if cited_year in cited_year_dict:
        cited_year_list = cited_year_dict.get(cited_year)
        cited_year_list += [filter_df['cited'].iloc[i]]
    else:
        cited_year_list = [filter_df['cited'].iloc[i]]
        cited_year_dict[cited_year] = cited_year_list
        
 """
Get a list of all the years a cited paper was published and sort the list, sort the data by year
"""
random_df = filter_df
pub_years = random_df['cited_pub_year'].unique()
pub_years = sorted(list(pub_years))
random_df = random_df.sort_values('cited_pub_year')

"""
Get all the papers cited in the earliest year, second earliest, etc. Each iteration shuffles the items and adds them to a list
"""
shuffle_list = []
for i in pub_years:
    cited_list = cited_year_dict.get(i)
    random.shuffle(cited_list)
    for j in cited_list:
        shuffle_list += [j]

random_df['shuffled'] = shuffle_list

# Test, prints the percent of citations that are different than original 
count = 0
for i in range(len(random_df)):
    if random_df['cited'].iloc[i] != random_df['shuffled'].iloc[i]:
        count += 1
edge_count = len(random_df)
print(round(100 - ((count / edge_count) * 100), 2))

# Get a list of edges
edge_list = []
# replace each doi with its integer index
for j in range(len(random_df)):
    edge = (random_df['citing'].iloc[j], random_df['cited'].iloc[j])
    edge_list += [(node_index.get(edge[0]), node_index.get(edge[1]))]
random_network = pd.DataFrame(edge_list)

random_network.to_csv('random_network.tsv', sep='\t',index=False, header=False)

