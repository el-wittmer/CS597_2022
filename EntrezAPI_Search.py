"""
El Wittmer
05.30.2022
modeled after code found here: https://techoverflow.net/2022/01/01/how-to-search-pubmed-entrez-api-with-python-and-filter-results-by-metadata/

Things that need changed: 
  ability to batch results as retmax gets maxed out at 10,000 search results. current approach is not scalable
  authors on individual lines
  
Note: Run time for a 5000 item search is longer than an hour
"""

import requests
import json
import time
import pandas

db = 'pubmed'
domain = 'https://www.ncbi.nlm.nih.gov/entrez/eutils'
nresults = 5000 # number of returned results
query = "(histone[Text Word])+AND+(English[Language])+AND+(\"1980\"[Publication Date] %3A \"1990\"[Publication Date])" # search terms
retmode='json'
retstart = 0 # starting index of search results, could be changed if necessary

eSearch = f'{domain}/esearch.fcgi?db={db}&retstart={retstart}&retmax={nresults}&retmode={retmode}&term={query}'
response = requests.get(eSearch)
pubmedJson = response.json()
results = []

for id in pubmedJson["esearchresult"]["idlist"]:
    queryLinkSummary = f'{domain}/esummary.fcgi?db={db}&id={id}&retmode={retmode}'
    metadata = requests.get(queryLinkSummary)
    # if there is an error message, don't try to access json
    metadata.raise_for_status()
    metadata = metadata.json()
    path = metadata["result"][f"{id}"]

    pubmed_id = id
    title = path["title"]
    publication_date = path["pubdate"]
    # format authors 
    authors = ""
    for i in range(len(path["authors"])):
      if "name" in path["authors"][i]:
        if i == len(path["authors"])-1:
          authors += path["authors"][i]["name"]
        else:
          authors += path["authors"][i]["name"] + ", "

    publication_type = path["pubtype"]

    # format article id and account for missing DOI
    # set DOI to none and update if DOI is found
    doi = None
    for i in range(len(path["articleids"])):
      if path["articleids"][i]["idtype"] == "doi":
        doi = path["articleids"][i]["value"]

    paper_meta = [pubmed_id,title,publication_date,authors,publication_type,doi]
    results += [paper_meta]
    # sleep to avoid server spam message
    time.sleep(.25)

header = ["PMID", "Title", "Publication Date", "Author(s)", "Publication Type", "DOI"]
csv_output = pandas.DataFrame(results, columns=header)
csv_output.to_csv('pubmed_results.csv', index=False)
# generates a csv that can then be copied to a text editor
csv_output
