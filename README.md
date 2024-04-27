# Technical Assesment


## Introduction
### Goal
The objective of this application is to retrieve data from an NIH API and serve it to a React Front End side in the form of a JSON object.

### Front End
![Front End Inputs](/frontend/public/FrontEndDisplay.png)
The React Front End of the app containts two input fields, one, to collect a query from the user and, the second, to input a list of IDs. The ID list is a result of making a request to the NIH API with the query inputted in the previous field. 

After a list of IDs have been inputted into the second text area, the user is redirected to a link, *http://127.0.0.1:5000/details*, which displays the complete JSON output for the requested IDs as shown below.

![JSON](/frontend/public/comprehensiveJSONoutput.png)

In order to view the concise details in a neatly formatted way, the user will need to click the 'back' arrow on the top of their browser to return to localhost:3000 where their output would have populated on the bottom of the screen as shown below. 

![Front End Inputs](/frontend/public/frontEndOutputOne.png)
![Front End Inputs](/frontend/public//FrontEndOutputTwo.png)

Each formatted Output Box features:
- PMID
- Article Title
- Journal Name
- Year Published
- Pagination
- Abstract
- Author List
- External Link to the Article

The Front End also has pagination support at the bottom that users can use to switch between multiple requests.

**PLEASE READ THE RUNNING THE APPLICATION SECTION BEFORE USING THE APP**
  
### Backend
The Backend of the application is written in python and uses the *requests* module to retrieve data from the NIH API. A *Flask* app is then used to post the retrieved information to the React Front End.

There are two Flask routes for this application, one to handle the ID requests and another to handle the Details requests.

``` python
@app.route("/queries", methods = ['POST'])
def queries():
    # start post request
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"

    # Example query "asthma[mesh] AND leukotrienes[mesh] 2009[pdat]"

    search_query = request.form['inputQuery']
    
    search_params = {
        "db": "pubmed",
        "term": f'{search_query}',
        "usehistory": "y",
        "retmode":"json",
    }
    search_post_response = requests.post(url = search_url, params=search_params)

    search_post_JSON = search_post_response.json()
    
    return search_post_JSON
```
The above code is the Flask application that handles the ID requests. The user input is stored in a variable called ```search_query``` and it is added to the ```search_params``` dictionary. This set of parametrs is passed on with the url to make a secure post request to the NIH API. The return mode is specified as JSON, and the returned data is stored in a variable called ```search_post_response```. This result is once again converted to JSON format, and it gets returned to the front end.

When a user uses this input in the front end, they will be redirected to a seperate link called *http://127.0.0.1:5000/queries*, and they will need to click the ***back arrow*** on their browser to input the list of IDs from *http://127.0.0.1:5000/queries* as shown below.

![List IDS](/frontend/public/listIDsOutput.png)

The second Flask app handles the details requests. When a user inputs the above list of IDs into the second input box, the Details Flassk ap uses the fetch url from the NIH API to retrieve detailed information about each article with the given ID.

```python
@app.route("/details", methods = ['POST'])
def details():
 
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed"
```
The inputted list is cleaned up and trimmed before it is stored in a parameter dictionary within a variable called ```no_sp_input_list``` shown below.

```python
details_params = {
        'id':f"{no_sp_input_list}",
        "retmode":"xml",
    }
    response = requests.get(url=fetch_url, params=details_params)
    response.raise_for_status()
    xml_dict  = xmltodict.parse(response.content)
```

The details for each request is returned in an XML format, so to convert it to JSON, I used a module called ```xmltodict```.

The above variable, ```xml_dict``` stores the JSON output for the list of requested articles.

I then used a for loop to traverse each article to gather the following JSON objects:
- PMID
- Article Title
- Journal Name
- Year Published
- Pagination
- Abstract
- Author List
- External Link to the Article

The code for this is as shown below:
```python
for index in range(len(xml_dict["PubmedArticleSet"]["PubmedArticle"])):
        try:
            PMID_path = xml_dict["PubmedArticleSet"]["PubmedArticle"][index]["MedlineCitation"]["PMID"]["#text"]
        except:
            PMID_path = "No data avilable for PMID"
        try:
            title_path = xml_dict["PubmedArticleSet"]["PubmedArticle"][index]["MedlineCitation"]["Article"]["ArticleTitle"]
        except:
            title_path = "No data avilable for ArticleTitle"
```
This ```try/except``` pattern continues for the rest of the gathered objects. I needed to use this error handling method since not all the articles had the needed information. 

Once this information was gathered, I wrote it as a JavaScript dictionary into a file called ```details.js```. This file ended up containing a JavaScript dictionary, called "details", with all the requested information for each article. The dictionary was then mapped to a React component called DetailOutputBox for each article. Every time a new input was made, the dictionary would be re-written.

```python
with open('../frontend/src/details.js', 'a') as file:
            file.write(f"\n{right_curly} id: \"{index}\", PMID: \"{PMID_path}\", Title: \"{title_path}\", Abstract: \"{abstract_path}\", AuthorList: \"{authorList_path}\", Journal: \"{journal_title_path}\",PublicationYear: \"{publication_year_path}\", MeSHTerms: \"{mesh_terms_path}\", Pagination: \"{pagination_path}\", ExternalLink: \"{external_link}\"{left_curly},")
```


***
## Known Defects
### Double Quotes
#### Problem
The largest pitfall of this application is that when writing data to the JavaScript dictionary, the JS Ditionary uses double quotes to identify the values of the dictionary. Therefore, any additional double quotes that are present in the JSON data interuppts the formatting of the dictionary and crashes the application since data can't be sent to the React Front End.

#### Current Solution
Since there is no clear way to predict when double quotes may be present in JSON data, the only current solution is to open up the details dictionarry and find the marked errors made by the code editor. The developer will then need to manually replace the double quotes with single quotes at the appropriate instances. Since this is only possible in a developer environment and not in production mode, it is safe to say that the program is not fit for deployment in its current condition. 

The below photo shows how just two double quotes in the highlighted region cause erros on neumerous lines.
![Sign Up Page Screenshot](/frontend/public/doubleQuoteError.png)

Now that those double quotes have been changed to single quotes as shown below, all the errors have dissappeared. 
![Sign Up Page Screenshot](/frontend/public/doubleQuoteSoln.png)

### Test Queries That Are Known to Work
```asthma[mesh] AND leukotrienes[mesh] 2009[pdat]```

```chimpanzee[orgn]+AND+biomol+mrna[prop]```

### Test IDs that are known to work
```20074456```, ```20046412```, ```19912318```, ```19895589```, ```19897276```, ```19894390```

### Test IDs that are known to cause Double Quote Errors
```20113659```, ```20008883``` 

There are other IDs that work and don't work, but these are just some tests you can use.
## Running the Application
### Download the uploaded code

Apart from the files that I have uploaded in the repository, you will also need to make sure you have the following dependencies:
1. node.js which you can download [here]('https://nodejs.org/en' "Node JS Download")
2. React, use the command ```npm start``` to open the React app
3. Navigate to the ```backend``` folder and install the following python dependencies:
   1. ```pip install requests```
   2. ```pip install xmltodict```
   3. ```pip3 install Flask```
4. Finally, make sure that you have this line ```"proxy":"http://http://127.0.0.1:5000"``` in your ```package.json``` folder as shown below on line 6. 

![Failure Page Screenshot](/frontend/public/proxyLine.png)

You will also need to edit some of the code in the `app.js` file. Starting around **line 43**, we see the following code block


## Sources Used 
While I had some prior knowledge about React before this Assesment, I learnt a lot while working on this project. In order to build this application out to the level that I was able to, I learnt about Flask, React{useState, useEffect}, React Pagination, and converting XML to JSON from the following videos.

- https://www.youtube.com/watch?v=7LNl2JlZKHA
- https://www.youtube.com/watch?v=wAGIOCqS8tk
- https://www.youtube.com/watch?v=Ntna1ndj8V4
  
While I did not copy any code line for line, I implement the concepts and logic used in those videos. 
***
