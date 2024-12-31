from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from scrapePrizePicks import prizepicks_api_fetch, get_final_data, get_pp_data
from scrapePropsCash import scrape_propcash_data, get_data_1
from checkBest import bestBets

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "yo chat we in the home domain (running all functions)"

@app.route('/prizepicks-api-fetch') #Scrapes Prizepicks Data
def prizepicks_api_fetch_data():
    return prizepicks_api_fetch()

@app.route('/prizepicks-api-data-send') #Gets Stored, Cleaned, Combined Data
def prizepicks_api_data_send():
    return jsonify(get_pp_data())


@app.route('/scrape-propcash-data') #Scrapes PropCash Data
def scrape_props():
    return scrape_propcash_data()
    
    
@app.route('/propcash-data') #Gets stored PropsCash data
def get_stored_data():
    return jsonify(get_data_1())

@app.route('/final-data-api')
def final_data_api():
    return jsonify(get_final_data())

@app.route('/get-best-lines')
def get_best_lines():
    return jsonify(bestBets())

if(__name__ == "__main__"):
    app.run(port=5001, host="0.0.0.0")