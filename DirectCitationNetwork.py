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

# only need the citing/cited columns
df2 = df[['citing', 'cited']]
# and a count of the number of times each cited paper is cited
df2 = df2.groupby('cited').count()
# this returns one column with two values in it, we need to fix that
df2.to_csv('cited_count.tsv', sep='\t', header=True)
df3 = pd.read_csv('cited_count.tsv', sep='\t', header=0)

# rename, sort so most highly cited on top
df3 = df3.rename(columns={'citing': 'count'})
df3 = df3.sort_values('count', ascending=False)

# in this data set, first 5 items are cited > 1000 times
df3 = df3.iloc[:4] # cited > 1000

# need to filter original data set to only include papers that cite the most highly cited papers
filtered_edges = []
for i in range(len(df)):
    if df['cited'].iloc[i] in filter_cited:
        filtered_edges += [(df['citing'].iloc[i], df['cited'].iloc[i])]
        
# create a new df with these edges and remove any duplicates
filter_df = pd.DataFrame(filtered_edges)
filter_df = filter_df.drop_duplicates()

# create a dictionary to convert doi to integer 
selected_columns = filter_df
temp = selected_columns.copy()
temp = temp.stack().reset_index()
node_list = temp[0].unique()

node_index = {}
for i in range(len(node_list)):
    node_index[node_list[i]] = i
   
# get a new list of edges that consists of integer ids rather than doi
edge_list = []
for j in range(len(filter_df)):
    edge = (filter_df['citing'].iloc[j], filter_df['cited'].iloc[j])
    edge_list += [(node_index.get(edge[0]), node_index.get(edge[1]))]

# and get a new df with integer edges
filter_df = pd.DataFrame(edge_list)

# finally, write tsv
filter_df.to_csv('filter_network.tsv', sep='\t',index=False, header=False)
