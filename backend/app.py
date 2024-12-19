from flask import Flask, jsonify
import csv
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)


global data_1
global data_2
data_1 = {}
data_2 = {}

@app.route('/')
def index():
    return "HI"

@app.route('/api-data')
def get_api_data():
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
        data_1 = data
        return jsonify(data)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api-data-2')
def get_api_bet_odds():
    global data_2

    API_URL = os.getenv('API_URL_2')
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
        data_2 = data
        return jsonify(data)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/stored-data')
def get_stored_data():
    global data_1
    return jsonify(data_1)

@app.route('/stored-data-2')
def get_stored_data_2():
    global data_2
    return jsonify(data_2)

if(__name__ == "__main__"):
    app.run(debug = True, port=5000)