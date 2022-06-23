import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np

histone_total = pd.read_csv('histone_export.csv') 
histone_citing = pd.read_csv('histone_citing_export.csv')
histone_cited = pd.read_csv('histone_cited_export.csv')

edge_number = histone_total.count()
print(f'The number of edges: {edge_number.iloc[0]}')

node_number =  pd.Series(data=histone_citing['citing'])
node_number = node_number.append(histone_cited['cited'])
print(f'The number of nodes: {node_number.nunique()}')

# for each node, find in/out degree and plot
import matplotlib.pyplot as plt

# V1 is missing year data 
df = pd.DataFrame(histone_total['cited'].value_counts()).join(histone_total['citing'].value_counts())
df.rename(columns = {'cited':'citations received', 'citing':'number of references'}, inplace = True)
plot = df.plot(kind='hist', logy=True)
plot.set_ylabel('frequency')
plt.show()

df.groupby('number of references').count()

histone_total['Pub_year'] = histone_total['publicationdate'].str[0:4]
selected_columns = histone_total[['cited', 'Pub_year']]
v2 = pd.DataFrame(data=(selected_columns))
v2 = v2.groupby('Pub_year').count()
v2

# data frame with avg in degree out degree for each decile in data set
df_agg = df
df_agg.rename(columns = {'citations received':'in degree', 'number of references':'out degree'}, inplace = True)

# labels DESC bc data descending by in degree
df_agg['decile'] = pd.cut(x=range(35337), bins=10, labels=[10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
df_agg = df_agg.groupby(['decile']).median()
df_agg
