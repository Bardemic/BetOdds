import requests
import os
from flask import jsonify


global data_1
data_1 = {}

def scrape_propcash_data():
    global data_1
    
    API_URL = os.getenv('API_URL_1')
    API_KEY = os.getenv('API_KEY')
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(API_URL, headers=headers)
        print(response)
        response.raise_for_status()
        data = response.json()
        for player in data:
            data_1[player["name"]] = player
        #data_1 = data
        return jsonify(data)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

def get_data_1():

    return data_1