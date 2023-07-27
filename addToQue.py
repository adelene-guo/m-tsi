import spotipy
from spotipy.oauth2 import SpotifyOAuth
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import threading

# --- Your Spotify Credentials ---
CLIENT_ID = '0eac05c214004561ab6bd69a504e2594'
CLIENT_SECRET = '008c275d524146d68a9ec0cd04540dfc'
REDIRECT_URI = 'http://10.102.194.37:8080/callback'
SCOPE = 'playlist-modify-private,playlist-modify-public,user-library-read'

# --- Local Server for Redirect ---

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        form = dict(parse_qs(query))
        self.server.return_values = form
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Received! You can close this window.")

def run_server():
    with socketserver.TCPServer(('localhost', 8080), RequestHandler) as server:
        server.handle_request()

# Start server in a thread
t = threading.Thread(target=run_server)
t.start()

# --- Spotify Authentication ---
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

# --- Functions to Search for Song URI and Add to Playlist ---

def search_song_uri(song_name):
    """Search for a song by name and return its URI."""
    result = sp.search(song_name, limit=1, type='track')
    tracks = result.get('tracks', {}).get('items', [])
    return tracks[0]['uri'] if tracks else None

def add_song_to_playlist(playlist_id, song_name):
    """Add a song to a specified playlist."""
    song_uri = search_song_uri(song_name)
    if song_uri:
        sp.playlist_add_items(playlist_id, [song_uri])
        print(f"Added {song_name} to playlist!")
    else:
        print(f"Could not find {song_name} on Spotify.")


# get playlist id
def get_playlist_id_by_name(sp, playlist_name):
    """
    Search for a playlist by name and return its ID.
    """
    results = sp.search(playlist_name, type='playlist', limit=50)  # you can adjust the limit
    for playlist in results['playlists']['items']:
        if playlist['name'] == playlist_name:
            return playlist['id']

    return None

# Example Usage:
# Assuming you have the playlist ID and a song name, you can use the following line to add it to the playlist:
playlist_ID = get_playlist_id_by_name(sp, "Verse")

add_song_to_playlist('playlist_ID', 'All of the lights')

# Please replace 'YOUR_PLAYLIST_ID' with your actual playlist ID and 'Despacito' with your desired song name.
