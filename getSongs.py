"""
Adie Guo
M&TSI 2023
7/26/23
"""

import os
import pandas as pd
import webbrowser
import spotipy
from spotipy import SpotifyOAuth
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import traceback
from jinja2 import Template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template
app = Flask(__name__)


# Get ID and secret from environment
client_id = "0eac05c214004561ab6bd69a504e2594"
client_secret = "008c275d524146d68a9ec0cd04540dfc"

# Replace with your machine's IP
YOUR_MACHINE_IP = "10.102.194.37"  # e.g., "192.168.x.x"
REDIRECT_URI = f"http://{YOUR_MACHINE_IP}:8000/callback"

# Set scope for API -- scope is to get top songs
scope = 'user-top-read'


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=REDIRECT_URI,
                                               scope=scope))



def clear_data_from_row_2(spreadsheet_name, worksheet_index=0):

    # Set up credentials
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\chase\Downloads\sixth-hawk-393504-f8baa14e8c72.json', scope)
    client = gspread.authorize(creds)

    # Open the specified spreadsheet
    spreadsheet = client.open(spreadsheet_name)
    worksheet = spreadsheet.get_worksheet(worksheet_index)

    # Get total rows
    num_rows = worksheet.row_count

    # Delete rows from 2 to the end
    if num_rows > 1:
        worksheet.delete_rows(2, num_rows)

    print(f"Cleared data from row 2 to end in '{spreadsheet_name}'!")

def get_album_cover():
  current_track = spotipy.current_playback()
  # Extract relevant information from the response
  if current_track:
        album_cover = current_track['item']['album']['images'][0]["url"]
        return album_cover
  else:
        return "No track is currently playing."

def add_song_to_playlist_by_name(song_name, sp_client):
    """Add a song to a specified playlist by its name."""
    playlist_name = "Verse"
    # Search for the playlist by name to get the playlist_id
    playlists = sp_client.current_user_playlists()
    playlist_id = None
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            playlist_id = playlist['id']
            break

    if not playlist_id:
        print(f"Could not find playlist named {playlist_name}")
        return

    # Search for the song by name to get the song_uri
    song_results = sp_client.search(q=song_name, type='track', limit=1)
    song_items = song_results['tracks']['items']

    if not song_items:
        print(f"Could not find song named {song_name}")
        return

    song_uri = song_items[0]['uri']

    # Add the song to the playlist
    sp_client.playlist_add_items(playlist_id, [song_uri])
    print(f"Added {song_name} to {playlist_name}!")

@app.route('/add_song', methods=['POST'])
def add_song():
    try:
        data = request.get_json()
        song_name = data['song_name']
        add_song_to_playlist_by_name(song_name, sp)
        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})



class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Extract the IP address of the client.
        ip = self.client_address[0]

        # If the path is the root, redirect to Spotify authentication
        if self.path == "/" or self.path == "":
            sp_temp = spotipy.Spotify(
                auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=REDIRECT_URI,
                                          scope=scope, cache_path=None))
            auth_url = sp_temp.auth_manager.get_authorize_url()
            self.send_response(302)  # 302 is a redirect status code
            self.send_header('Location', auth_url)
            self.end_headers()
            return


        # Check if the path is /callback
        elif self.path.startswith("/callback"):
            # Use the client's IP as part of the cache file name
            cache_file = f".cache-{ip}"
            # Create a dynamic Spotipy client inside the callback
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                           client_secret=client_secret,
                                                           redirect_uri=REDIRECT_URI,
                                                           scope=scope,
                                                           cache_path=cache_file))
            #add_song_to_playlist_by_name('Verse', 'All of the lights', sp)

            # Extract the code from the callback URL
            query_components = parse_qs(urlparse(self.path).query)
            code = query_components.get("code", [None])[0]

            # ... [rest of your code remains unchanged]

            if code:
                print(f"Received code: {code}")
                try:
                    # Get the access token using the code
                    token_info = sp.auth_manager.get_access_token(code)
                    if token_info:
                        sp.token = token_info["access_token"]
                    else:
                        print("Failed to retrieve access token using code.")
                        # handle the error, perhaps by redirecting the user to authenticate again

                    # Get the current authenticated user's username
                    current_user_info = sp.me()
                    username = current_user_info["id"]

                    # Fetch the user's top tracks
                    top_tracks = sp.current_user_top_tracks(limit=10, time_range='short_term')
                    data = {
                        "Track Name": [track["name"] for track in top_tracks["items"]],
                        "Artist": [", ".join([artist["name"] for artist in track["artists"]]) for track in
                                   top_tracks["items"]],
                        "Album": [track["album"]["name"] for track in top_tracks["items"]],
                        "Release Date": [track["album"]["release_date"] for track in top_tracks["items"]]
                    }

                    # Convert to DataFrame
                    df = pd.DataFrame(data)
                    print("Fetched top tracks and created DataFrame")

                    # Set up credentials for google API
                    google_scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
                    creds = ServiceAccountCredentials.from_json_keyfile_name(
                        r'C:\Users\chase\Downloads\sixth-hawk-393504-f8baa14e8c72.json', google_scope)
                    client = gspread.authorize(creds)

                    # Open spreadsheet
                    spreadsheet = client.open('userSongs')
                    worksheet = spreadsheet.get_worksheet(0)
                    existing_data = worksheet.get_all_values()
                    start_row = len(existing_data) + 1
                    worksheet.append_rows(df.values.tolist(), value_input_option='RAW', insert_data_option='OVERWRITE',
                                          table_range=f'A{start_row}')

                    print("Data added to Google Sheets")

                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    with open("verse_user.html", "r") as file:
                        template = Template(file.read())
                        rendered_html = template.render(
                            num_tracks=len(df),
                            TRACK_NAME=df["Track Name"].tolist(),
                            ARTIST=df["Artist"].tolist(),
                            ALBUM=df["Album"].tolist(),
                            RELEASE_DATE=df["Release Date"].tolist()
                        )

                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(rendered_html.encode())
                    return
                except Exception as e:

                    print(f"Error while processing: {e}")
                    traceback.print_exc()  # This will print the full traceback
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(b"Internal server error!")
                    return

            else:
                print("Failed to obtain code from callback!")
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Failed to authenticate!")
                return

        # If it's neither root nor callback, serve files as usual
        else:
            super().do_GET()

if __name__ == '__main__':
    # Start the HTTP server
    with socketserver.TCPServer(("", 8000), MyHTTPRequestHandler) as httpd:
        clear_data_from_row_2('userSongs')
        clear_data_from_row_2('playlist')
        print(f"Server started at http://{YOUR_MACHINE_IP}:8000")
        print("http running")
        link = "http://{YOUR_MACHINE_IP}:8000"
        httpd.serve_forever()
    #app.run()


