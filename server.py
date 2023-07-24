from flask import Flask, request, redirect
import spotipy
from spotipy import SpotifyOAuth

app = Flask(__name__)

# Spotipy setup
client_id = "0eac05c214004561ab6bd69a504e2594"
client_secret = "008c275d524146d68a9ec0cd04540dfc"
redirect_uri = "https://e407-2607-f470-6-1001-4db8-ffe8-b900-cf79.ngrok-free.app/callback"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='user-top-read'))

@app.route('/callback')
def callback():
    # Extract the code from the query parameters
    code = request.args.get('code')

    if not code:
        return "No code provided by Spotify. Please try again.", 400

    try:
        # Use Spotipy to get the token
        token_info = sp.auth_manager.get_access_token(code, check_cache=False)
        access_token = token_info['access_token']

        # Now, you can use this token to access Spotify data
        sp = spotipy.Spotify(auth=access_token)
        # ... (rest of your logic to get user's top tracks, etc.)

        return "Data fetched successfully!"
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(port=8000)
