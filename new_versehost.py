from flask import Flask, render_template_string, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
        

        <!-- Adie Guo M&TSI 2023 7/26/23 -->
        
        <!DOCTYPE html>
        <html lang="en-US">
        
        <head>
            <title>verse</title>
            <link rel="stylesheet" type="text/css" href="verse_user.css">
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Jacques+Francois&display=swap" rel="stylesheet">
            <script>
                            function runScript() {
                                fetch('/run-script', {
                                    method: 'POST', // specify it's a POST request here
                                })
                                .then(response => response.json())
                                .then(data => alert(data.message))
                                .catch(error => console.error('Error:', error));
                            }
            </script>
        </head>
        
        <body style="background-color: #151414; margin-left: 7%; margin-right: 7%; margin-top: 7%; margin-bottom: 7%;">
            
            <div style="margin-top: 3%"></div>
            <center><button onclick="runScript()" style="color:#151414; width: 35%;">CREATE PLAYLIST</button><center>
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