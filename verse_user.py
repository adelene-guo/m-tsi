from flask import Flask, render_template_string, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
<html lang="en-US">
<title>verse</title>
<head>
    <link rel="stylesheet" type="text/css" href="verse_user.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Jacques+Francois&display=swap" rel="stylesheet">
    
</head>

<body style="background-color: #151414; margin-left: 7%; margin-right: 7%; margin-top: 7%; margin-bottom: 7%;">
    <div style="margin-top: 3%"></div>
    
    <center><img src="verse_title.png" width="40%"></center>

    <div style="margin-top: 3%"></div>
    <b><span style="display: inline; color:#CC5500; font-size: 50px;" id="number"></span></b>
    <p style="display: inline;"> contributors</p>

    <div style="margin-top: 3%"></div>
    <div style="float: left;">currently playing...</div>

    <div style="float: right;">
        mixing
        <label class="switch" id="mixingOn" onclick="mixingOn()">
            <input type="checkbox">
            <span class="slider round"></span>
        </label>
    </div>

    <div style="margin-top: 15%"></div>
    <center><img src="SongCoverExample.jpeg" alt="Song Cover" width="40%"></center>

    <div style="margin-top: 3%"></div>
    <h1 style="text-align: center;" id="songName"></h1> <!--code this part-->

    <div id="queue-container">
        <h2>your top songs</h2>
        <div style="width: 100%; overflow-x: auto;">
            <table style="background-color: #151414; color: #CC5500; width: 100%; margin-bottom: 2%;">
                {% for index in range(num_tracks) %}
                <tr style="width: 100%;">
                    <td style="display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 8px 0;
                    border-bottom: 1px solid #CC5500;">{{ TRACK_NAME[index] }} by {{ ARTIST[index] }}</td>
                </tr>
                {% endfor %}
            </table>
            <h2>added songs</h2>
            <ul id="queue-list"></ul>
            <input type="text" id="song-input" style ="color: #151414;width:32.5%" placeholder="song name">
            <input type="text" id="artist-input" style ="color: #151414;width:32.5%" placeholder="artist">
            <button style="color:#151414; width: 14%;" onclick="addSong()">add</button>
      
        </div>
        
    </div>
    <Center><button style="color:#151414; width: 25%;" onclick="clearQueue()">clear queue</button></Center>
    <script src="verse_user.js"></script>
    
</body>

</html>
 ''')

@app.route('/run-script', methods=['POST'])
def run_script():
    print("got to run script function")
    try:
        print("got to try")
        # Assuming your main script is named 'makeSpotifyPlaylist.py'
        subprocess.check_call(["python", "makeSpotifyPlaylist.py"])
        return jsonify({"message": "Script ran successfully!"})
    except subprocess.CalledProcessError:
        print("exception")
        return jsonify({"message": "Error running script!"}), 500

if __name__ == '__main__':
    app.run(debug=True)
    print("running app")