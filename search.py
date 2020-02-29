from settings import my_api_key, my_cse_id
from googleapiclient.discovery import build
import json
import re


def google_search(search_term, api_key, cse_id, **kwargs):
    '''Send query to google search..
    '''
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res

def extract(q, emails_collected, start_index):
	''' Extract the emails & looping next pages.. 
	'''
	result = google_search(q, my_api_key, my_cse_id, start=start_index)

	try:
		for i in result['items']:
			collected = re.findall(r'[\w\.-]+@[\w\.-]+', i['snippet'])
			for h in collected:
				emails_collected.append(h)
	except:
		pass

	try:
		start_index = result['queries']['nextPage'][0]['startIndex']
		if start_index < 101: #100:
			extract(q, emails_collected, start_index)	
	except:
		pass


def g_search(q):
	'''
	Main function for gathering all the results
	'''
	emails_collected = []
	extract(q,emails_collected,1)
	#finally, removing duplicates
	emails_collected = list(set(emails_collected)) 
	return emails_collected