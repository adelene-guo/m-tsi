"""
Chase Leibowitz
M&TSI 2023
Spotify API Testing
Create a playlist in my spotify account using Spotify API

"""
"""import os
import requests
import base64

# get ID and secret from environment
client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
SPOTIFY_CREATE_PLAYLIST_URL = "https://api.spotify.com/v1/users/{user_id}/playlists"

# print id and secret to test that we got them

def get_access_token(client_id, client_secret):

    data = {
        'grant_type': 'client_credentials'
    }
    auth_header = base64.b64encode((client_id + ":" + client_secret).encode()).decode()
    auth_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(auth_url, headers={"Authorization": "Basic " + auth_header}, data=data)
    access_token = response.json().get('access_token')
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        print("Access Token:", access_token)
    else:
        print("Error:", response.status_code, response.text)
    return access_token

def create_playlist(ACCESS_TOKEN, name, public):
    response = requests.post(
        SPOTIFY_CREATE_PLAYLIST_URL,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        },
        json={
            "name": name,
            "public": public
        }

    )
    json_resp = response.json()

    return json_resp

token = get_access_token(client_id, client_secret)


playlist = create_playlist(token, name="test playlist", public=False)
print(f"Playlist: {playlist}")"""

import os
import requests
import base64
import webbrowser

# Get ID and secret from environment
client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]

REDIRECT_URI = "http://localhost:8000/callback"  # replace with your callback URL
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_CREATE_PLAYLIST_URL = "https://api.spotify.com/v1/users/{user_id}/playlists"

params = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": "playlist-modify-private"  # necessary scope to create private playlists
}

# Open the authorization URL in a web browser for the user to grant permissions
webbrowser.open(requests.Request('GET', AUTH_URL, params=params).prepare().url)

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

auth_code = input("Paste the authorization code here: ")
token = get_access_token(auth_code)

def create_playlist(ACCESS_TOKEN, user_id, name, public):
    response = requests.post(
        SPOTIFY_CREATE_PLAYLIST_URL.format(user_id=user_id),
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        },
        json={
            "name": name,
            "public": public
        }
    )

    return response.json()




# Note: You need the user_id (Spotify username) to create a playlist for them.
user_id = input("Enter your Spotify username (user_id): ")
playlist = create_playlist(token, user_id, name="test playlist", public=False)
print(f"Playlist: {playlist}")
