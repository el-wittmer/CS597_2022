import pandas as pd

# read in both leng data and personal data of citations to paul
nodes = pd.read_csv("~/Downloads/Leng_2022_Nodes.csv", header=0)
WoS_Check = pd.read_csv("Paul_WoS_IDs.tsv", sep='\t')

# extract the WoS IDs from WoS_Check
WoS_Check = pd.Series(WoS_Check['UT'])
WoS_Check = WoS_Check.tolist()

# compare against the leng data. if not present, add to list
check = []
for id in range(len(nodes)):
    if nodes['WoS_ID'].iloc[id] not in WoS_Check:
        check += [nodes['Id'].iloc[id]]
        
# remove Paul et al. [1963] from list
check.remove(1)

# print the ids of the mismatches
print(check)
