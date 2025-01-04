import requests
import os
from flask import jsonify


global data_nfl
global data_nba
global data_nhl
data_nba = {}
data_nfl = {}
data_nhl = {}

def scrape_propcash_data(league):
    print("scrape_propcash_data")
    global data_nfl
    global data_nba
    global data_nhl
    
    NFL_URL = os.getenv('API_URL_1')
    NBA_URL = os.getenv('API_URL_2')
    NHL_URL = os.getenv('API_URL_3')
    API_KEY = os.getenv('API_KEY')

    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        if league == 9:
            API_URL = NFL_URL
        elif league == 7:
            API_URL = NBA_URL
        elif league == 8:
            API_URL = NHL_URL
        response = requests.get(API_URL, headers=headers)
        print(response)
        response.raise_for_status()
        data = response.json()
        if league == 9:
            for player in data:
                data_nfl[player["name"]] = player
        elif league == 7:
            for player in data:
                data_nba[player["name"]] = player
        elif league == 8:
            for player in data:
                data_nhl[player["name"]] = player
        return jsonify(data)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

def get_data_nfl():
    global data_nfl
    return data_nfl
def get_data_nba():
    global data_nba
    return data_nba
def get_data_nhl():
    global data_nhl
    return data_nhl
def reset_variables_pc():
    global data_nfl
    global data_nba
    global data_nhl
    data_nfl = {}
    data_nba = {}
    data_nhl = {}
