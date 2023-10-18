#
#
#created by Kirk Ogunrinde on June 7, 2023

#install and import BeautifulSoup library. #Beautiful Soup relies on a parser so I had to install lxml to parse the HTML files 
from bs4 import BeautifulSoup

#install and import requests library. Requests is used to send requests to websites and recieve responses
import requests

#import urljoin and urlparse to parse the HTML
from urllib.parse import urljoin, urlparse, urlsplit

#the function extractLinksXTitles is defined with a parameter links of type ResultSet from the bs4.element module. 
#this indicates that the function expects an object of type ResultSet as an argument.
#the function iterates over the allLinks: ResultSet parameter of  as if it were a list or iterable. 
#each item in the ResultSet represents an HTML element matching the specified search criteria.
from typing import List
from bs4.element import ResultSet

#import csv to write outputs to csv file
import csv

#import os to help code interact with the operating system the code is running on
import os

#import nltk libraries to assist in stemming and tokenisation
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

#import sentence_transformers lubrary to utilise BERT for semantic similarity
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer("bert-base-uncased")

#import string
import string




















###############################################################################################################
#FUNCTION DEFINITIONS

#function that makes a url-HTMLtext-links map
def extractURLsXHTML_textXlinks(url, HTMLWithoutTags, allLinks):
    

    # Create a dictionary to store the URL, HTML text, and links
    URLsXHTML_textXlinksMap = {
        'url': url,
        'tokenisedWords': cleanUpHTML(HTMLWithoutTags),
        'links': verifyLinks(allLinks)
    }
    
    return URLsXHTML_textXlinksMap



#function that tokenises, stems and cleans up the HTML text and returns them in a list
def cleanUpHTML(html_text):
    # Remove punctuations
    html_text = html_text.translate(str.maketrans("", "", string.punctuation))
    
    # Tokenize the text into individual words and convert them to lowercase
    tokens = [token.lower() for token in word_tokenize(html_text)]
    
    # Initialize WordNetLemmatizer for word lemmatization
    lemmatizer = WordNetLemmatizer()
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    
    # Apply lemmatization and remove stopwords while preserving the lowercase format
    tokenized_words = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    
    return tokenized_words



#function that checks links to see if they are valid and downloadable
def verifyLinks(listOfLinks):
    
    # List of allowed extensions for links
    allowed_extensions = [".pdf", ".csv", ".xlsx", ".doc", ".txt", ".ppt", ".pptx", ".zip", ".ashx", "download"]
    
    #create new list to store valid links
    valid_links = []
    
    # Check each link in allLinks
    for link in listOfLinks:
        # Parse HTML
        soup = BeautifulSoup(str(link), "html.parser")
        
        # Find the first <a> anchor tag in the parsed HTML content
        checkATag = soup.a
        
        # If there are no <a> tags, continue to the next link
        if checkATag is None:
            continue
        
        # Retrieve the value of the href attribute (link) using the .get() method
        href = checkATag.get("href")
        
        # Make sure the link has a valid href
        if href is not None:
            # Make sure the link is complete. If not, add the base URL using urljoin
            if not href.startswith("http://") and not href.startswith("https://"):
                href = urljoin(base_url, href)
            
            # Make sure the link ends with a valid extension
            if any(href.endswith(extension) for extension in allowed_extensions):
                valid_links.append(href)

    return valid_links


#function that calculates the sim score based on a user query using BERT
def calculateSimScore(query_embedding, html_embeddings):
    
    # Calculate cosine similarity between query and HTML embeddings
    sim_scores = util.pytorch_cos_sim(query_embedding, html_embeddings)
    
    return sim_scores


#function that prints out the map of urls X HTMLs X links into a csv
def print_map_to_csv(data_map):
    
    with open('map_data.csv', 'w', newline='') as csvfile:
        
        writer = csv.writer(csvfile)
        writer.writerow(['URL', 'HTML', 'Link'])
        
        for item in data_map:
            writer.writerow([item['url'], item['tokenisedWords'], item['links']])



#function to calculate the similarities between the query and the url
def calculateURLSimilarities(final_results, query, model):
    
    #encode the query using the sentence_transfomer model
    query_tokens = model.encode([query], convert_to_tensor=True)
    
    #map url_similarities to store urls and their similarity scores to the user query
    url_similarities = {}
    
    
    for tokenisedHTML in final_results:
        
        #retrieves the tokenised words from the map
        tokenized_words = tokenisedHTML['tokenisedWords']
        
        #encodes the tokenised words using the sentence transformer model
        url_tokens = model.encode([tokenized_words], convert_to_tensor=True)
        
        #caluculates cosine similarity between encoded query and encoded URL tokens
        sim_scores = util.pytorch_cos_sim(query_tokens, url_tokens)
        
        #retrieves the similarity score from sim_scores and converts to python float
        similarity_score = sim_scores[0].item()
        
        #adds to url_smilarities dict, where the key is the url and the value is similarity score between query and HTML
        url_similarities[tokenisedHTML['url']] = similarity_score


    return url_similarities






















###############################################################################################################
#MAIN CODE

#new array URL_List will take in URLs from a csv file.
URLList = []

#get the path of the current script using os library's .path
scriptDirectory = os.path.dirname(os.path.abspath(__file__))
csvFilePath = os.path.join(scriptDirectory, "urls.csv")

#construct path to csv file
csvFilePath = os.path.join(scriptDirectory, "urls.csv")

#open csv file with read mode "r"
with open("urls.csv", "r") as file:
    
    #create new csv reader object
    csv_reader = csv.reader(file)
    
    #iterate over each row in the csv file
    for row in csv_reader:
        
        #assuming each url is saved in the first box 
        url = row[0]
        
        #add the url to the list
        URLList.append(url)


#print out the list to be sure
print()
for index, item in enumerate(URLList):
    print(f"{index + 1}. {item}")


#take in user query
print()
query = input("Enter Query Here: ")
print("You entered:", query)

finalResults = []

for url in URLList:
    
    #if the url starts with a BOM, then remove the first character
    if url.startswith("\ufeff"):
        url = url[1:]
        
    
    resultFromWebsite = requests.get(url)
    
    # Use urlsplit to get the base_url of the webpage
    base_url = urlsplit(url).scheme + "://" + urlsplit(url).netloc

    #use .text which converts html codes into readable text
    content = resultFromWebsite.text

    #parse HTML file in BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

    # Extract text from HTML and remove all tags
    #get_text() method removes both the HTML tags and the content of the tags, including element tags
    HTMLWithoutTags = soup.get_text()
    
    #find all links on the website using HTML searchterm "<a>" and the .find_all() and save them to a list "allLinks"
    #.find_all() returns list in HTML format
    allLinks = soup.find_all("a")
     
    #call extractURLsXHTML_textXlinks with the url, HTML text, and allLinks to have map of url X HTML words X links
    #the fucntion also returns the html_embeddings
    mapResult = extractURLsXHTML_textXlinks(url, HTMLWithoutTags, allLinks)
    finalResults.append(mapResult)
    
    #call print_map_to_csv to print out the map to a file
    print_map_to_csv(finalResults)
    
    #call calculate similarity score to calculate the similarity score between the query and the urls in the corpus
    urlSimilarities = calculateURLSimilarities(finalResults, query, model)

    # Sort the URLs based on the similarity scores in descending order
    sorted_urls = sorted(urlSimilarities, key=urlSimilarities.get, reverse=True)

    # Check if the current iteration is the last iteration
    is_last_iteration = (url == URLList[-1])

    # If it's the last iteration, print the similarity scores in the sorted order
    if is_last_iteration:
        print("Similarity Scores:")
        for url in sorted_urls:
            similarity_score = urlSimilarities[url]
            print()
            print(f"{url}: {similarity_score}")
            print()
    
 