from flask import Flask, request

app = Flask(__name__)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if code:
        print(f"Received authentication code: {code}")
        return "Authentication successful! You can close this window."
    else:
        return "Error receiving authentication code."

if __name__ == '__main__':
    app.run(debug=True, port=8000)
    print("running")