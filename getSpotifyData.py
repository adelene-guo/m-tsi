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


# links and stuff idrk man -- i don't think im using these anymore
REDIRECT_URI = "http://localhost:8000/callback"  # replace with your callback URL
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

# set scope for API -- scope is to get top songs
scope = 'user-top-read'
redirect_uri = 'http://localhost:8000/callback'

# Create a spotipy client -- replacing this code bc deprecated
#token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

# do the actual spotify API thing to get the top tracks -- prepare loader and send request
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope, cache_path=".cache-" + username))
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
