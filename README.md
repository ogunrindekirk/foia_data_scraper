This project scrapes websites by deriving href tags from the HTMLs and storing both the link and the titles of all the links on the page. The project uses the BeautifulSoup library for the parsing. User only has to enter a URL to derive links and titles. 

# DOJ_web_scraping
1. Working on scraping DOJ, DHS, and DOD websites to find FOIA links to important/ frequently asked documents.
2. Downloading and creating a database of FOIA logs from DOJ, DOD, and DHS websites. 

# Successes
We completed a scraper that can derive links and their titles from a URL for websites which have the URL embedded in the document title. We were also able to save the files and the links into a pdf/ xlsx/ csv file after scraping. I edited the code to utilise a different functionality - maps. I used the Title and Link to the documents as key-value pairs and created a function that produced the results after taking in a bs4 list of HTML formatted link tags.

# Failures
Websites are not standardised, so the scraper struggles with sites which do not have the URL embedded in the document title. We have compiled a list of these websites that would require either manual entry or a customisation of the scraping functionality for them. The link can be accessed [here](https://drive.google.com/drive/folders/1Stt5pE_qak2Ak1MA8a33-TEqzuQOo8Qn).

# Next Steps
We have discussed a plan to move forward with obtaining the FOIA logs and scraping the websites. We have been able to finish the categorisation for the websites which can be easily scraped and those which can not. They are located in the second sheets of the component logs in the drive folder (the Google sheets, and not the document files). By tomorrow, we would have started downloading the FOIA logs for the DHS and DOD. After then, we can begin the website scraping for those easily-scrapable websites.
