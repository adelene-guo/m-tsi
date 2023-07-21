import os
import pandas as pd
import webbrowser
import spotipy
import spotipy.util as util

# Get ID and secret from environment
client_id = "0eac05c214004561ab6bd69a504e2594"
client_secret = "008c275d524146d68a9ec0cd04540dfc"
#username = "h1dcv8yl4w1l1egbsf4x9dnx2"  # Replace with your Spotify username



# links and stuff idrk man
REDIRECT_URI = "http://localhost:8000/callback"  # replace with your callback URL
#AUTH_URL = 'https://accounts.spotify.com/authorize'
#TOKEN_URL = 'https://accounts.spotify.com/api/token'

# set scope
scope = 'user-top-read'
redirect_uri = 'http://localhost:8000/callback'

# Create a spotipy client using user's access token
def create_spotipy_client(username):
    token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    sp = spotipy.Spotify(auth=token)
    return sp

# Get the user's Spotify username from the cache
def get_spotify_username():
    sp = create_spotipy_client(None)
    user_info = sp.current_user()
    return user_info["id"]

"""# Create a spotipy client
token = util.prompt_for_user_token(None, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth=token)"""


username = get_spotify_username()
sp = create_spotipy_client(username)

# get top tracks
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
print(df)

# df to excel
file_name = "top_tracks.xlsx"
df.to_excel(file_name, index=False)

# Open the Excel file
os.system(f"start {file_name}")
