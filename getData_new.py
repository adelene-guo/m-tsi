# imports
import os
import requests
import base64
import webbrowser
import pandas as pd
import os
import spotify as sp

# Get ID and secret from environment
client_id = "0eac05c214004561ab6bd69a504e2594"
client_secret = "008c275d524146d68a9ec0cd04540dfc"

# links and stuff idrk man
REDIRECT_URI = "http://localhost:8000/callback"  # replace with your callback URL
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

#params for request
params = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": "user-top-read"  # necessary scope to create private playlists
}

SPOTIFY_GET_TOP_TRACKS_URL = "https://api.spotify.com/v1/me/top/tracks"


# get data
def get_top_tracks(ACCESS_TOKEN, limit=10, time_range='medium_term'):
    """
    Get a user's top tracks.

    Parameters:
    - limit: The number of entities to return. Range: 1-50. Default: 10.
    - time_range: Over what time frame the affinities are computed.
                  Valid values: 'long_term' (several years), 'medium_term' (last 6 months),
                  'short_term' (last 4 weeks). Default: 'medium_term'
    """

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    params = {
        "limit": limit,
        "time_range": time_range
    }

    response = requests.get(SPOTIFY_GET_TOP_TRACKS_URL, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()["items"]
    else:
        print("Error:", response.status_code, response.text)
        return []

# get token
def get_access_token(auth_code):
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print("Error:", response.status_code, response.text)
        return None



# authorize on web
webbrowser.open(requests.Request('GET', AUTH_URL, params=params).prepare().url)

# enter in auth code from web, get token, get user id
auth_code = input("Paste the authorization code here: ")
token = get_access_token(auth_code)
user_id = input("Enter your Spotify username (user_id): ")

# Example usage:
top_tracks = get_top_tracks(token)
data = {
    "Track Name": [track["name"] for track in top_tracks],
    "Artist": [track["artists"][0]["name"] for track in top_tracks],
    "Album": [track["album"]["name"] for track in top_tracks],
    "Popularity":[track["album"]["popularity"] for track in top_tracks],
    "song_id":[track["album"]["id"] for track in top_tracks],
    "Release Date": [track["album"]["release_date"] for track in top_tracks]
}


# get data into df
df = pd.DataFrame(data)
print(df)

features = {}
all_track_ids = list(df['song_id'].unique())
start = 0
num_tracks = 10
while start < len(all_track_ids):
    tracks_batch = all_track_ids[start:start+num_tracks]
    features_batch = sp.audio_features(tracks_batch)
    features.update({ track_id : track_features 
                 for track_id, track_features in zip(tracks_batch, features_batch) })
    start += num_tracks

print(features['1mqlc0vEP9mU1kZgTi6LIQ'])

# df to excel
file_name = "top_tracks.xlsx"
df.to_excel(file_name, index=False)

# Open excel file
os.system(f"start {file_name}")

