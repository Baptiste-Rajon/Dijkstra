from flask import Flask, request, jsonify
from flask_cors import CORS

import json
import dijkstra

app = Flask(__name__)
CORS(app) 

def log_toggle_state(toggle_name, state):
    print(f"{toggle_name}: {state}")



@app.route('/data', methods=['POST'])
def process_data():
    data = request.get_json()
    print("Données reçues:", data)

    with open("config.json", "r", encoding="utf-8") as config_file: 
        CONFIGURATION = json.loads(config_file.read())
    CONFIGURATION["start"] = data.get("Src")
    CONFIGURATION["end"] = data.get("Dst")
   
    with open("config.json", "w") as file_config:
        file_config.write(json.dumps(CONFIGURATION, indent=4))

    response = dijkstra.main()
    
    return jsonify(response), 200

@app.route('/stat1', methods=['POST']) 
def stat1():
    with open("config.json", "r", encoding="utf-8") as config_file: 
        CONFIGURATION = json.load(config_file)
   
    data = request.json
    print(data)
    toggle1_state = data.get('shorter_wanted', False)
    toggle2_state = data.get('lower_wanted', False)

    log_toggle_state("Toggle 1", "ON" if toggle1_state else "OFF")
    log_toggle_state("Toggle 2", "ON" if toggle2_state else "OFF")

    print(toggle1_state)
    CONFIGURATION["shorter_wanted"] = toggle1_state
    CONFIGURATION["lower_wanted"] = toggle2_state

    import connector
    connector.test(CONFIGURATION)
    return jsonify(CONFIGURATION)


if __name__ == '__main__':
    app.run(host='localhost', port=1235)
