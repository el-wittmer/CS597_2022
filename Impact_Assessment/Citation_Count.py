import pandas as pd
import matplotlib as plt

# get the Paul data from each breadth and depth file generated 
tl = pd.DataFrame(columns = ["fp_int_id", "cp_level", "cp_r_citing_zero", "cp_r_citing_nonzero", "tr_citing", "cp_r_cited_zero", "cp_r_cited_nonzero", "tr_cited"])
for year in range(1964, 1984): 
    temp = pd.read_csv(f"Timeline_Metrics/networkit_bdid-{year}.csv")
    tl = tl.append(temp.iloc[1:2])
    
# create a year column for the data frame    
years = []
for i in range(1964, 1985):
    years += [int(i)]
tl["year"] = years

# rename columns
tl = tl[["cp_level", "cp_r_citing_zero", "cp_r_citing_nonzero", "year"]]
tl = tl.rename(columns={"cp_level": "citation_count", "cp_r_citing_zero": "breadth", "cp_r_citing_nonzero": "depth"})

# restrict data to year and citation count
cite_count = tl[['citation_count', 'year']]

ax = cite_count_year.plot(x="year", figsize=(8, 6), legend=False)
ax.set_xlabel("Year")
ax.set_ylabel("Citations Earned per Year")
ax.set_xticks([1964, 1969, 1974, 1979, 1984])
ax.set_ylim(0, 35)
