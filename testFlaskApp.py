from flask import Flask, render_template_string, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
        <html>
            <head>
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
            <body>
                <button onclick="runScript()">Run Script</button>
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
