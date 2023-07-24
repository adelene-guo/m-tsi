# imports
import os
import requests
import base64
import webbrowser
import pandas as pd
import os
from flask import Flask
from flask import request

# Get ID and secret from environment
client_id = "0eac05c214004561ab6bd69a504e2594"
client_secret = "008c275d524146d68a9ec0cd04540dfc"

# links and stuff idrk man
REDIRECT_URI = "http://localhost:8000/callback"  # replace with your callback URL
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

redirect_app = Flask(__name__)


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





