"""
Chase Leibowitz
M&TSI 2023
7/21/23
Get the user's top tracks from the Spotify API and save it as dataframe
"""

import os
import pandas as pd
import webbrowser
import spotipy
import spotipy.util as util
from spotipy import SpotifyOAuth

# Get ID and secret from environment
client_id = "0eac05c214004561ab6bd69a504e2594"
client_secret = "008c275d524146d68a9ec0cd04540dfc"
username = "h1dcv8yl4w1l1egbsf4x9dnx2"  # Replace with your Spotify username

REDIRECT_URI = 'https://e407-2607-f470-6-1001-4db8-ffe8-b900-cf79.ngrok-free.app/callback'

# set scope for API -- scope is to get top songs
scope = 'user-top-read'

# Create the SpotifyOAuth object
sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=REDIRECT_URI, scope=scope, cache_path=".cache-" + username)

# Get the authentication URL
auth_url = sp_oauth.get_authorize_url()

# Print the authentication URL
print("Open the following URL on your phone or any other device:")
print(auth_url)

# Pause script execution to give you time to authenticate on another device
input("Press Enter once authenticated...")

# Continue the script once authenticated
token_info = sp_oauth.get_cached_token()  # This gets the token from the cache

if not token_info:
    print("Could not retrieve token. Please ensure authentication was successful.")
    exit()

# Create Spotify client with the token
sp = spotipy.Spotify(auth=token_info['access_token'])

top_tracks = sp.current_user_top_tracks(limit=10, time_range='short_term')

# organize the data
data = {
        "Track Name": [track["name"] for track in top_tracks["items"]],
        "Artist": [", ".join([artist["name"] for artist in track["artists"]]) for track in top_tracks["items"]],
        "Album": [track["album"]["name"] for track in top_tracks["items"]],
        "Release Date": [track["album"]["release_date"] for track in top_tracks["items"]]
    }

# get data into df
df = pd.DataFrame(data)

# print the df so i can see it and make sure everything worked
print(df)

# convert DF to excel file and open -- not currently using
# convert DF to excel file -- not using right now
#file_name = "top_tracks.xlsx"
#df.to_excel(file_name, index=False)

# Open the Excel file
#os.system(f"start {file_name}")
