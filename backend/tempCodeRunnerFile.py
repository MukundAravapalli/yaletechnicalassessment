from flask import Flask
import requests, pandas as pd, xmltodict, json, untangle


# start post request
search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"

search_query = "asthma[mesh] AND leukotrienes[mesh] 2009[pdat]"
# list_of_ids = requests.get(url = input_url)
search_params = {
    "db": "pubmed",
    "term": f'{search_query}',
    "usehistory": "y",
    "retmode":"json",
}
search_post_response = requests.post(url = search_url, params=search_params)
search_post_JSON = search_post_response.json()
print(f"search_post_output:\n{search_post_JSON}")

list_of_ids = search_post_JSON["esearchresult"]["idlist"]
print(f"\n\nlist_of_ids {list_of_ids}")