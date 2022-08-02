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

# calculate ratio of breadth/depth for each year
tl['depth ratio'] = tl.apply(lambda row: row.depth / row.citation_count, axis=1)
tl['breadth ratio'] = tl.apply(lambda row: row.breadth / row.citation_count, axis=1)

# save only required columns
tl_bd = tl[["breadth ratio", "depth ratio", "year"]]

# formatting graph
font = {'family' : 'normal',
        'size'   : 18}

plt.rc('font', **font)

ax = tl_bd.plot(x="year", figsize=(8,6))
ax.set_ylabel("Breadth to Depth Ratio")
ax.set_xlabel("Year")
ax.axhline(y=0.5, color="grey")
ax.set_xticks([1964, 1969, 1974, 1979, 1984])
