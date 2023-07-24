from flask import Flask, request

app = Flask(__name__)

# Flask route for handling the callback
@app.route('/callback')
def callback():
    auth_code = request.args.get('code')
    token = get_access_token(auth_code)
    if token:
        # Example usage:
        top_tracks = get_top_tracks(token)
        data = {
            "Track Name": [track["name"] for track in top_tracks],
            "Artist": [track["artists"][0]["name"] for track in top_tracks],
            "Album": [track["album"]["name"] for track in top_tracks],
            "Release Date": [track["album"]["release_date"] for track in top_tracks]
        }

        # get data into df
        df = pd.DataFrame(data)
        print(df)

        # df to excel
        file_name = "top_tracks.xlsx"
        df.to_excel(file_name, index=False)

        return "Authentication successful. Data retrieved and processed."
    else:
        return "Authentication failed."

if __name__ == "__main__":
    app.run(debug=True)