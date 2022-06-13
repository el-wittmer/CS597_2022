"""
El Wittmer
05.24.22

Given a list of DOIs, returns a csv containing DOI and title.
"""

from habanero import Crossref
import pandas as pd

# Set up
cr = Crossref()
source = pd.read_csv('/content/gdrive/My Drive/Colab Notebooks/Files/k50dois.csv')
dois_to_list = source['doi'].tolist()
df = pd.DataFrame(columns=['DOI', 'Title'])

# Batching
increment = 35
lower_bound = 0
upper_bound = increment

while upper_bound <= len(source):
  # in the case where len(source) % increment != 0, some remainder will need to be accounted for
  if len(source) - upper_bound < increment:
    upper_bound = len(source)

  a = cr.works(ids= dois_to_list[lower_bound : upper_bound])

  for i in range(len(a)):
    df = df.append({'DOI' : a[i]['message']['DOI'], 'Title' : a[i]['message']['title']}, ignore_index = True)

  lower_bound += increment
  upper_bound += increment

df.to_csv('title_results.csv', index=False)
df
