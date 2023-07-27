"""
Chase Leibowitz
M&TSI 2023
7/21/23

This script takes the user's favorite songs from the cloud from the downloadData script, uploads it to the GPT 3.5 Turbo API,
and then gets a return of similar songs. The script then cleans the data and prints it.
"""

import openai
import requests
import pandas as pd
from downloadData import df, len_data
print(df)

songs = df['Track Name'].to_string(index=False)
#print(songs)



import openai
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from downloadData import df, len_data

# Set up Google Sheets API authentication
def authenticate_gsheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\chase\Downloads\sixth-hawk-393504-f8baa14e8c72.json', scope)
    client = gspread.authorize(creds)
    return client

# Function to update the Google Sheet
def update_sheet(client, songs_list):
    sheet = client.open("playlist").sheet1
    for idx, song in enumerate(songs_list, start=2):  # start=2 to begin at row 2
        sheet.update_cell(idx, 1, song)  # Updates column 1 (or 'A')
# function to ask ChatGPT
def ask_GPT(input, key):
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
    }

    data = {
        "model": "gpt-3.5-turbo",  # Change this to the desired model (e.g., "gpt-3.5-turbo")
        "messages": [{"role": "system", "content": "Output a list of 10 songs that are very similar to those inputted to you. Your only output will be a list of the exact song names. Do not include the number before each song. Do not include the artist name. Just 10 song names seperated by lines. Do not include a title to your message or a note after the songs. The songs must not be the same as the ones inputted to you."},
                     {"role": "user", "content": input}]
    }

    response = requests.post(api_url, headers=headers, json=data)


    response_data = response.json()
    return response_data

key = "sk-jaOG1kzVUNYqdEMOOumNT3BlbkFJRe16TPWTlXpMmwsDD2ZV"

response = ask_GPT(songs, key)
print(response)

print('\n\ncreating AI playlist...\n')
assistant = response['choices'][0]['message']['content']


# print the new songs
print(assistant)

# Parse the assistant string to extract individual songs
# Assuming each song is on a new line, you can split by newline:
new_songs_list = assistant.split('\n')
df = pd.concat([df, pd.DataFrame({'Track Name': new_songs_list})], ignore_index=True)


# Authenticate and update the sheet
client = authenticate_gsheets()
update_sheet(client, df['Track Name'])

# print the new songs
print(assistant)