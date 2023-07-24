from flask import Flask, request, redirect, jsonify
import spotipy
from spotipy import SpotifyOAuth

app = Flask(__name__)

# Your Spotify app details
client_id = '0eac05c214004561ab6bd69a504e2594'
client_secret = '008c275d524146d68a9ec0cd04540dfc'
# Assuming you're using port 8000, replace the IP address with the public IP of your AWS EC2 instance
redirect_uri = 'http://3.145.106.251:8000/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope='user-top-read'))

@app.route('/')
def index():
    return '<a href="/login">Login to Spotify</a>'

@app.route('/login')
def login():
    auth_url = sp.auth_manager.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp.auth_manager.get_access_token(request.args['code'], check_cache=False)
    top_tracks = sp.current_user_top_tracks(limit=10, time_range='short_term')
    return jsonify(top_tracks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
