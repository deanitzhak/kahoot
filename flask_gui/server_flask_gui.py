from flask import Flask, render_template, jsonify
import requests
import threading
import time

# a flask server that will serve the GUI for the game 
# and will poll the game server for the players' status
# will run automatically when the docker container is started
app = Flask(__name__)

players_data = []
url = "http://localhost:5001/get_status"

def poll_server():
    global players_data
    while True:
        try:
            response = requests.get(url)  
            if response.status_code == 200:
                players_data = response.json()
        except requests.RequestException as e:
            print(f"Error polling server: {e}")
        time.sleep(1)  

polling_thread = threading.Thread(target=poll_server)
polling_thread.daemon = True
polling_thread.start()

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/get_status')  
def get_players():
    return jsonify(players_data)  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
