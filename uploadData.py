"""
Chase Leibowitz
M&TSI 2023
7/21/23
Take the dataframe from getSpotifyData and upload it to a spreadsheet in google drive
"""

# import stuff
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe

# import df from getSpotifyData -- run getSpotifyData
from getSpotifyData import df




# Set up credentials for google API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\chase\Downloads\sixth-hawk-393504-f8baa14e8c72.json', scope)
client = gspread.authorize(creds)

# Open spreadsheet
spreadsheet = client.open('test')

# figure out where to start working -- index of where to start working in the spreadsheet -- add somethign later to start after other stuff


# add stuff to make it just append to spreadsheet instead of replacing -- online help
worksheet = spreadsheet.get_worksheet(0)

existing_data = worksheet.get_all_values()
start_row = len(existing_data) + 1
worksheet.append_rows(df.values.tolist(), value_input_option='RAW', insert_data_option='OVERWRITE', table_range=f'A{start_row}')

"""# Clear existing data -- maybe get rid of it later when we have multiple devices
worksheet.clear()

# add df data to spreadsheet/worksheet thingy
set_with_dataframe(worksheet, df, include_column_header=True)"""
