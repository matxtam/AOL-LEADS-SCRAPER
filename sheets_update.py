from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from search import g_search
from settings import SPREADSHEET_ID


def connect(SCOPES):
    """Connects sheets API
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service

def sheet_search(SPREADSHEET_ID):
    '''Search sheets names
    '''
    sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = sheet_metadata.get('sheets', '')
    title = sheets[0].get("properties", {}).get("title", "Sheet1")
    sheet_id = sheets[0].get("properties", {}).get("sheetId", 0)
    return sheets

def read(SPREADSHEET_ID,RANGE_NAME):
    '''Search Column Names
    '''
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])
    return values

def write(SPREADSHEET_ID, values, write_range):
    '''Write emails collected to sheet
    '''
    body = {
        'values': values
    }
    value_input_option = 'RAW'
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=write_range,
        valueInputOption=value_input_option, body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

def values_to_column(h,values):
    '''Format list to write in sheet
    '''
    new_list = [[h.split('"')[1]]]
    for x in values:
        new_list.append([x])
    print (new_list)
    input()
    return new_list

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

###The main process
#Connecting to Google Sheets API
service = connect(SCOPES)

num_to_col = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR  ','AS','AT','AU','AV','AW','AX','AY','AZ','BA','BB','BC','BD','BE','BF','BG','BH','BI','BJ','BK','BL','BM','BN']
#Search sheets names
sheets = sheet_search(SPREADSHEET_ID)
for i in sheets[1:]:
    state = i['properties']['title']
    RANGE_NAME = state + '!A:A' 
    #Read Column names
    values_read = read(SPREADSHEET_ID, RANGE_NAME)
    col = 0
    for h in values_read[1:]:
        h = h[0]
        #Make Google search query
        q= h 
        #Invoke Google Search function and format values
        values = values_to_column(h,g_search(q))
        col += 1
        col_name = num_to_col[col]
        #Write Emails in Sheet
        write_range = state + '!' + col_name + ':' + col_name 
        write(SPREADSHEET_ID,values,write_range)

    #print('next state')