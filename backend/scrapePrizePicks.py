import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from flask import jsonify
from scrapePropsCash import get_data_1
from bet import Bet
from datetime import datetime

global pp_data
global pp_data_bet_objs
global final_data_bet_objs
global final_data
global last_updated
pp_data = []
pp_data_bet_objs = [] #Stores the data, but in the Bet class format
final_data = []
final_data_bet_objs = []
last_updated = datetime(2000, 1, 1, 1, 1, 1, 1)

def prizepicks_api_fetch():
    print("prizepicks_api_fetch ran")
    global pp_data
    global pp_data_bet_objs
    global final_data
    global final_data_bet_objs
    global last_updated
    data_1 = get_data_1()

    selenium_address = os.environ.get('SELENIUM_LOCATION')

    options = Options() #using selenium vs request because of Prizepick's restrictions, cannot deploy to a docker with requests (and if you could, my 10 hours of trying wasn't enough smh)
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Remote(command_executor=f'http://{selenium_address}:4444/wd/hub', options=options)
    driver.set_page_load_timeout(5)
    driver.get("https://api.prizepicks.com/projections?league_id=9&per_page=250&single_stat=true&in_game=true&state_code=IL&game_mode=pickem")
    while driver.execute_script("return document.readyState") != "complete":
        pass
    data = json.loads(driver.find_element(By.XPATH, "/html/body").text)
    driver.quit()


    
    pp_data = []
    pp_data_bet_objs = []
    final_data = []
    final_data_bet_objs
    for bet in data["data"]:
        for player in data["included"]:
            #return jsonify({"1": player["id"], "2": bet["relationships"]["new_player"]["data"]["id"]})
            if "name" in player["attributes"] and player["id"] == bet["relationships"]["new_player"]["data"]["id"]:
                this_bet = Bet(player["attributes"]["name"], bet["attributes"]["line_score"], player["id"], bet["attributes"]["stat_type"])
                #return jsonify(this_bet.to_dict())
                pp_data_bet_objs.append(this_bet)
                pp_data.append(this_bet.to_dict())
    
    for prize_pick_bet in pp_data_bet_objs:
        #return prize_pick_bet.player_name 
        if prize_pick_bet.player_name in data_1.keys():
            if prize_pick_bet.projection_type in data_1[prize_pick_bet.player_name].keys(): #I should DEFFO clean this up tbh
                prize_pick_bet.set_info(
                    data_1[prize_pick_bet.player_name][prize_pick_bet.projection_type]["l10Rate"],
                    data_1[prize_pick_bet.player_name][prize_pick_bet.projection_type]["vsOpp"],
                    data_1[prize_pick_bet.player_name][prize_pick_bet.projection_type]["currentSeason"],
                    data_1[prize_pick_bet.player_name][prize_pick_bet.projection_type]["under"],
                    data_1[prize_pick_bet.player_name][prize_pick_bet.projection_type]["over"]
                )#l10, h2h, in2024
                final_data.append(prize_pick_bet.to_dict_final())
                final_data_bet_objs.append(prize_pick_bet)
    last_updated = datetime.now()
    return jsonify(data)

def get_pp_data():
    return pp_data
def get_pp_data_bet_objs():
    return pp_data_bet_objs
def get_final_data():
    return final_data
def get_final_data_bet_objs():
    global final_data_bet_objs
    return final_data_bet_objs
def get_last_time_updated():
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    global last_updated
    time_table = {
        "year": last_updated.year,
        "month": months[last_updated.month - 1],
        "day": last_updated.day,
        "hour": last_updated.hour,
        "minute": last_updated.minute,
        "second": last_updated.second
    }
    return time_table

def reset_variables_pp():
    global pp_data
    global pp_data_bet_objs
    global final_data_bet_objs
    global final_data
    pp_data = []
    pp_data_bet_objs = []
    final_data_bet_objs = []
    final_data = []

