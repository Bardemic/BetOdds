from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from scrapePrizePicks import prizepicks_api_fetch, get_final_data_nfl, get_final_data_nba, get_final_data_nhl, get_last_time_updated, reset_nba_pp, reset_nfl_pp, reset_nhl_pp, get_pp_data_nba, get_pp_data_nfl, get_pp_data_nhl
from scrapePropsCash import scrape_propcash_data, get_data_nfl, get_data_nba, get_data_nhl, reset_variables_pc
from checkBest import bestBets
from flask_apscheduler import APScheduler


class Config:
    SCHEDULER_API_ENABLED = True

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config())
CORS(app)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


        

@scheduler.task('cron', id='do_job_1', minute='*/15')
def job1():
    with app.app_context():
        reset_nba_pp()
        reset_nfl_pp()
        reset_nhl_pp()
        reset_variables_pc()
        scrape_propcash_data(7)
        scrape_propcash_data(8)
        scrape_propcash_data(9)
        prizepicks_api_fetch(7)
        prizepicks_api_fetch(8)
        prizepicks_api_fetch(9)
    print('Job 1 executed')

@app.route('/update-all')
def update_all():
        reset_nba_pp()
        reset_nfl_pp()
        reset_nhl_pp()
        reset_variables_pc()
        scrape_propcash_data(7)
        scrape_propcash_data(8)
        scrape_propcash_data(9)
        prizepicks_api_fetch(7)
        prizepicks_api_fetch(8)
        prizepicks_api_fetch(9)
        return "complete!"



@app.route('/')
def index():
    return "yo chat we in the home domain (running all functions)"

@app.route('/prizepicks-api-fetch-nfl') #Scrapes Prizepicks Data
def prizepicks_api_fetch_data():
    return prizepicks_api_fetch(9)

@app.route('/prizepicks-api-fetch-nba')
def prizepicks_api_fetch_nba():
    return prizepicks_api_fetch(7)

@app.route('/prizepicks-api-fetch-nhl')
def prizepicks_api_fetch_nhl():
    return prizepicks_api_fetch(8)

@app.route('/prizepicks-api-data-send-nfl') #Gets Stored, Cleaned, Combined Data
def prizepicks_api_data_send_nfl():
    return jsonify(get_pp_data_nfl())

@app.route('/prizepicks-api-data-send-nba') #Gets Stored, Cleaned, Combined Data
def prizepicks_api_data_send_nba():
    return jsonify(get_pp_data_nba())

@app.route('/prizepicks-api-data-send-nhl') #Gets Stored, Cleaned, Combined Data
def prizepicks_api_data_send_nhl():
    return jsonify(get_pp_data_nhl())


@app.route('/scrape-propcash-data-nfl') #Scrapes PropCash Data
def scrape_props_nfl():
    return scrape_propcash_data(9)

@app.route('/scrape-propcash-data-nba') #Scrapes PropCash Data
def scrape_props_nba():
    return scrape_propcash_data(7)

@app.route('/scrape-propcash-data-nhl') #Scrapes PropCash Data
def scrape_props_nhl():
    return scrape_propcash_data(8)

@app.route('/get-last-updated')
def get_updated():
    return get_last_time_updated()
    
    
@app.route('/propcash-data-nfl') #Gets stored PropsCash data
def get_stored_data_nfl():
    return jsonify(get_data_nfl())

@app.route('/propcash-data-nba') #Gets stored PropsCash data
def get_stored_data_nba():
    return jsonify(get_data_nba())

@app.route('/propcash-data-nhl') #Gets stored PropsCash data
def get_stored_data_nhl():
    return jsonify(get_data_nhl())

@app.route('/final-data-nba-api')
def final_data_nba_api():
    return jsonify(get_final_data_nba())

@app.route('/final-data-nhl-api')
def final_data_nhl_api():
    return jsonify(get_final_data_nhl())

@app.route('/final-data-nfl-api')
def final_data_nfl_api():
    return jsonify(get_final_data_nfl())

@app.route('/get-best-lines-nfl')
def get_best_lines_nfl():
    return jsonify(bestBets(9))

@app.route('/get-best-lines-nhl')
def get_best_lines_nhl():
    return jsonify(bestBets(8))

@app.route('/get-best-lines-nba')
def get_best_lines_nba():
    return jsonify(bestBets(7))
if(__name__ == "__main__"):
    app.run(port=5001, host="0.0.0.0")