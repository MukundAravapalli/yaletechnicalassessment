from flask import Flask, request
import requests,  xmltodict, json


app = Flask(__name__)

@app.route("/queries", methods = ['POST'])
def queries():
    # start post request
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"

    # search_query = "asthma[mesh] AND leukotrienes[mesh] 2009[pdat]"
    search_query = request.form['inputQuery']
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
    
    return search_post_JSON


@app.route("/details", methods = ['POST'])
def details():
 
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed"
 
    details_input_string = request.form['idList']
    split_details_input = details_input_string.split(",")

    no_sp_input_list = []
    for list_item in split_details_input:
        new_item = list_item.strip()
        no_sp_input_list.append(new_item)

    print(f"no_sp_input_list: {no_sp_input_list}")

    details_params = {
        'id':f"{no_sp_input_list}",
        "retmode":"xml",
    }
    response = requests.get(url=fetch_url, params=details_params)
    response.raise_for_status()
    xml_dict  = xmltodict.parse(response.content)
    details_JSON = json.dumps(xml_dict)

    right_curly = "{"
    left_curly = "}"

    with open('../frontend/src/details.js', 'w') as file:
        file.write(f"let details = [ ")


    for index in range(len(xml_dict["PubmedArticleSet"]["PubmedArticle"])):
        try:
            PMID_path = xml_dict["PubmedArticleSet"]["PubmedArticle"][index]["MedlineCitation"]["PMID"]["#text"]
        except:
            PMID_path = "No data avilable for PMID"
        try:
            title_path = xml_dict["PubmedArticleSet"]["PubmedArticle"][index]["MedlineCitation"]["Article"]["ArticleTitle"]
        except:
            title_path = "No data avilable for ArticleTitle"
        try:
            abstract_path = xml_dict["PubmedArticleSet"]["PubmedArticle"][index]["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]
        except:
            abstract_path = "No data avilable for Abstract"
        try:
            authorList_path = xml_dict["PubmedArticleSet"]["PubmedArticle"][index]["MedlineCitation"]["Article"]["AuthorList"]
        except:
            authorList_path = "No data avilable for Author List"
        try:
            journal_title_path = xml_dict["PubmedArticleSet"]["PubmedArticle"][index]["MedlineCitation"]["Article"]["Journal"]["Title"]
        except:
            journal_title_path = "No data avilable for Journal Title"
        try:
            publication_year_path = xml_dict["PubmedArticleSet"]["PubmedArticle"][index]["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]["Year"]
        except:
            publication_year_path = "No data avilable for Publication Year"
        try:
            mesh_terms_path = xml_dict["PubmedArticleSet"]["PubmedArticle"][index]["MedlineCitation"]["MeshHeadingList"]
        except:
            mesh_terms_path = "No data avilable for MeSH Terms"
        try:
            pagination_path = xml_dict["PubmedArticleSet"]["PubmedArticle"][index]["MedlineCitation"]["Article"]["Pagination"]
        except:
            pagination_path = "No data avilable for Pagination"
        try:
            external_link = f"https://pubmed.ncbi.nlm.nih.gov/{PMID_path}/"
        except:
            external_link = "No external link avilable"



        with open('../frontend/src/details.js', 'a') as file:
            file.write(f"\n{right_curly} id: \"{index}\", PMID: \"{PMID_path}\", Title: \"{title_path}\", Abstract: \"{abstract_path}\", AuthorList: \"{authorList_path}\", Journal: \"{journal_title_path}\",PublicationYear: \"{publication_year_path}\", MeSHTerms: \"{mesh_terms_path}\", Pagination: \"{pagination_path}\", ExternalLink: \"{external_link}\"{left_curly},")
    

    with open('../frontend/src/details.js', 'a') as file:
        file.write(f"\n];\nexport default details;")

    return xml_dict


if __name__ == "__main__":
    app.run(debug=True)