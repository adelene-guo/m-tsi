"""
Chase Leibowitz, Adie & Others
M&TSI 2023
7/26/2023

This script does the following:
1. Downloads user song data from the 'userSongs' worksheet in a Google spreadsheet
2. Sends the user song data to GPT-3.5 Turbo API to get similar songs
3. Combines the user songs and the AI suggested songs
4. Uses Spotify API to add the combined songs to a playlist
5. Saves the metadata of the tracks in the playlist to an Excel file
"""

# Libraries
import pandas as pd
import gspread
import requests
import spotipy
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe
from spotipy.oauth2 import SpotifyOAuth
import os

# ---- GOOGLE SHEET SECTION ----
# Credentials for Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\chase\Downloads\sixth-hawk-393504-f8baa14e8c72.json', scope)
client = gspread.authorize(creds)

# Download data from Google Sheets
spreadsheet = client.open('playlist')

# Extracting user songs
worksheet_user_songs = spreadsheet.worksheet('userSongs')
df_user_songs = get_as_dataframe(worksheet_user_songs, evaluate_formulas=True, skiprows=0).dropna(how='all').dropna(axis=1, how='all')
user_songs = df_user_songs['Track Name'].to_string(index=False)

# ---- GPT-3.5 TURBO API SECTION ----
# GPT-3.5 function to get similar songs
def ask_GPT(input, key):
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}"}
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a DJ for an event. You will read the songs that are sent as the input and then create a playlist that is double the length of the songs inputted that will be in similar style and taste to the songs submitted. None of the songs you give will be the same as the ones I feed to you"},
            {"role": "user", "content": input}
        ]
    }
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()

key = "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"  # Replace with your OpenAI key
response = ask_GPT(user_songs, key)
ai_playlist = response['choices'][0]['message']['content'].split('\n')

# Combine user songs and AI songs
combined_songs = list(df_user_songs['Track Name']) + ai_playlist

# ---- SPOTIFY SECTION ----
# Spotify credentials
SPOTIPY_CLIENT_ID = '0eac05c214004561ab6bd69a504e2594'  # Replace with your Spotify Client ID
SPOTIPY_CLIENT_SECRET = '008c275d524146d68a9ec0cd04540dfc'  # Replace with your Spotify Client Secret
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="playlist-modify-private,playlist-modify-public"))
user_id = sp.current_user()['id']

# Create new playlist and add songs
playlist = sp.user_playlist_create(user_id, "Verse", public=True)
playlist_id = playlist['id']
added_track_ids = []
track_df = pd.DataFrame(columns=['ID', 'Album Cover', 'Duration (ms)', 'Popularity', 'Danceability', 'Energy', 'Valence', 'Key', 'Tempo', 'Time Signature'])

for song in combined_songs:
    if not song or pd.isna(song):  # Check for empty or NaN values
        continue

    try:
        search_result = sp.search(song, limit=1, type='track')
        track = search_result['tracks']['items'][0]
        track_id = track['id']

        # Check for duplicates before adding
        if track_id not in added_track_ids:
            # Get audio features for the track
            audio_features = sp.audio_features(track_id)[0]

            # Append data to the dataframe
            track_df.loc[track_id] = {
                'ID': track_id,
                'Album Cover': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'Duration (ms)': track['duration_ms'],
                'Popularity': track['popularity'],
                'Danceability': audio_features['danceability'],
                'Energy': audio_features['energy'],
                'Valence': audio_features['valence'],
                'Key': audio_features['key'],
                'Tempo': audio_features['tempo'],
                'Time Signature': audio_features['time_signature']
            }

            sp.playlist_add_items(playlist_id, [track_id])
            added_track_ids.append(track_id)
            print("added: " + str(song))
        else:
            print(f"Duplicate song {song} skipped.")
    except IndexError:
        print(f"Couldn't find {song} on Spotify.")
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error searching for {song}. Error: {e}")

print(track_df)

# Save data to Excel
file_name = "output.xlsx"
with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
    track_df.to_excel(writer, sheet_name='Sheet1', index=False)

# Open Excel
os.system(f'start excel "{file_name}"')  # for Windows
