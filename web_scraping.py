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

###
#FUNCTION DEFINITIONS

#define a function to extract the titles and real links from the HTML format
#function takes the HTML format of the links and titles and returns a map of title and link as key-value pair
#dict is essentially a map in python 
def extractLinksXTitles(allLinks: ResultSet) -> dict[str, str]: 
    
    #create empty map link_map
    ultimateMap = {}
    
    # List of allowed file extensions
    allowed_extensions = [".pdf", ".csv", ".xlsx", ".doc", ".txt", ".ppt", ".pptx", ".zip", ".ashx", "download"]
    
    #for each index in the list, create a key-value pair
    for link in allLinks:
        
        #parse HTML
        soup = BeautifulSoup(str(link), "html.parser")
                             
        #selects the first <a> anchor found in the parsed HTML content                 
        checkATag = soup.a
        
        #if there are no <a> tags, then there is no link to extract and the code continues to next index
        if checkATag is None:
            continue
        
        #retrieves the value of the href attribute (link) using the .get() method
        link = checkATag.get("href")
        
        #retrieves the text content using the .text property. .strip() then removes any leading or trailing spaces
        title = checkATag.text.strip()
        
        # remove unnecessary whitespace from the title
        title = " ".join(title.split())
        
        #make sure link has a valid href
        if link is not None:
            
            #make sure that the link is complete. If not, add the base url using urljoin
            if not link.startswith("http://") and not link.startswith("https://"):
                link = urljoin(base_url, link)
            
            #make sure that the link ends with the valid endings
            if any(link.endswith(extension) for extension in allowed_extensions):
                ultimateMap[title] = link
        
    return ultimateMap
    

    
#define a function that takes in a map and prints out items to a csv file
def printToCSV(data, filename) :
    
    #use os class"s get.cwd() to get the current directory where the script is being executed
    directory = os.getcwd()
    
    # create complte filepath by joining the "directory" and "filename" together
    filepath = os.path.join(directory, filename)
    
    #assigns what I want to be the headers to the csv file to variable headerNames
    headerNames = ["Title", "Link"]
    
    #open csvfile specified by variable "filepath" in writemode using open(), hence the "w"
    #the as keyword assigns a name to the object returned by a function
    with open(filepath, "w", newline="") as csvfile:
        
        #creates a csv.Dictwriter object named header to write to csvfile, specifying the file and the headerNames
        #csv.DictWriter class allows writing data to a CSV file using maps, where the keys represent the field names 
        #and the values represent the corresponding data
        header = csv.DictWriter(csvfile, fieldnames=headerNames)
        
        #writes header row to csv file based on "header" variable. 
        #writeheader() is called on the header object to write the header row
        header.writeheader()
        
        for title, link in data.items():
            header.writerow({"Title": title, "Link": link})
    
    








#MAIN CODE

#array URL_List takes in website https
URL_List = [""]
#use .get() method from requests library to request result information from all websites in URL_List array 
#and perform scraping on them
    
    
for url in URL_List:
    resultFromWebsite = requests.get(url)
    
    # Use urlsplit to get the base_url of the webpage
    base_url = urlsplit(url).scheme + "://" + urlsplit(url).netloc

    #use .text which converts html codes into readable text
    content = resultFromWebsite.text

    #parse HTML file in BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

    #TEMPORARY: print out content to check
    #print(soup.prettify())
    
    #find all links on the website using HTML searchterm "<a>" and the .find_all() and save them to a list "allLinks"
    #.find_all() returns list in HTML format
    allLinks = soup.find_all("a")
         
     
    #call extra extract_linksXtitles with allLinks to print map of title X links
    finalResult = extractLinksXTitles(allLinks) 

    # Generate a unique filename for each URL using the netloc component of the URL
    # Remove any non-alphanumeric characters from the netloc and add the .csv extension
    filename = f"{urlsplit(url).netloc}.csv"

    #call printToCSV to print the finalResult list to filename with unique filename 
    printToCSV(finalResult, filename)

    #iterate over map and print items
    for title, link in finalResult.items():
        print(f"Title: {title}")
        print(f"Link: {link}")
        print()
