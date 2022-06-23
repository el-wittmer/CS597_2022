import pandas as pd
import matplotlib

citation_data = pd.read_csv(f'histone_export.csv')

dictionary = {}

for i in range(len(citation_data)):
  citing_paper = citation_data['citing'][i]
  if citing_paper in dictionary:
    # save keys (citations) from citing paper
    cited_list = dictionary.get(citing_paper)
    # add the cited paper to the list
    cited_list += [citation_data['cited'][i]]
    # add key : updated citing list back into the dictionary
    dictionary[citing_paper] = cited_list
  else:
    # add new key : value pair
    dictionary[citing_paper] = [citation_data['cited'][i]]
    
count_dict = {}
for i in dictionary:
    # get the list of cited papers
    ref_list = dictionary.get(i)
    if len(ref_list) > 1:
        # find each combination of cited papers
        for j in range(len(ref_list)):
            for k in range(j+1, len(ref_list)):
                pair = (ref_list[j], ref_list[k])
                pair = sorted(pair)
                pair = tuple(pair)
                # if the given combination isn't in the dictionary, add a new key. Else increase the value by one.
                if pair not in count_dict:
                    count_dict[pair] = 1
                else:
                    count_dict[pair] += 1

df = pd.DataFrame(list(count_dict.items()), columns=['Pair', 'Count'])
df = df.sort_values('Count')
df.to_csv('result.csv')

ax = df.plot(kind="hist", logy=True)
ax.set_xlabel('Frequency of Co-Citation')
ax.set_ylabel('Number of Pairs')
ax.get_legend().remove()
