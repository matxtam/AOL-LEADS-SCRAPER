# EMAIL LEADS SCRAPER

Little scrapper for populating a Google Sheets sheet automatically. Based on Python3, Google Sheets Api and Google Search Api.


## Installation

>$ pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib


### Enable google sheets api

Go to https://developers.google.com/sheets/api/quickstart/python  
Hit 'Enable Google Sheets Api'  
Download 'credentials.json' and move to app directory.  

### Enable google search api

Go to https://developers.google.com/custom-search/v1/overview  
Hit 'Get a Key'  
Select 'Quickstart'  
Copy 'YOUR API KEY' and replace the variable 'my_api_key' in the settings.py file  

### Create Google Custom Search Engine

Go to https://cse.google.com/all  
Sites to search: 'www.google.com'  
Name of the search engine: 'search'  
Hit on 'Control Panel'  
Turn 'Search the entire web' ON  
Copy 'Search engine ID' and replace the variable 'my_cs_key' in the settings.py file.  
Hit 'Custom Search JSON API'/ 'Get started' to check payed plans.  

### Spreadsheet ID 

Replace SPREADSHEET_ID variable with the Spreadsheet ID in the settings.py file.  

## Execute

>$ sheets_update.py


