import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from flask import jsonify
from scrapePropsCash import get_data_nfl, get_data_nba, get_data_nhl
from bet import Bet
from datetime import datetime
from extension import proxies
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

global pp_data_nfl
global pp_data_bet_objs_nfl
global final_data_nfl
global final_data_bet_objs_nfl
global pp_data_nba
global pp_data_bet_objs_nba
global final_data_bet_objs_nba
global final_data_nba
global pp_data_nhl
global pp_data_bet_objs_nhl
global final_data_nhl
global final_data_bet_objs_nhl
global last_updated
pp_data_nfl = []
pp_data_bet_objs_nfl = [] #Stores the data, but in the Bet class format
final_data_nfl = []
final_data_bet_objs_nfl = []
pp_data_nba = []
pp_data_bet_objs_nba = [] #Stores the data, but in the Bet class format
final_data_nba = []
final_data_bet_objs_nba = []
pp_data_nhl = []
pp_data_bet_objs_nhl = [] 
final_data_nhl = []
final_data_bet_objs_nhl = []
last_updated = datetime(2000, 1, 1, 1, 1, 1, 1)

def prizepicks_api_fetch(league): #7 is NBA, #9 is NFL, #8 is NHL
    print("prizepicks_api_fetch ran")
    global pp_data_nfl
    global pp_data_bet_objs_nfl
    global final_data_nfl
    global final_data_bet_objs_nfl
    global pp_data_nba
    global pp_data_bet_objs_nba
    global final_data_bet_objs_nba
    global final_data_nba
    global pp_data_nhl
    global pp_data_bet_objs_nhl
    global final_data_nhl
    global final_data_bet_objs_nhl
    global last_updated
    data_nfl = get_data_nfl()
    data_nba = get_data_nba()
    data_nhl = get_data_nhl()

    selenium_address = os.environ.get('SELENIUM_LOCATION')
    proxy_user = os.environ.get('PROXY_USER')
    proxy_pass = os.environ.get('PROXY_PASS')
    proxy_ip = os.environ.get('PROXY_HOST')
    proxy_port = os.environ.get('PROXY_PORT')

    options = Options() #using selenium vs request because of Prizepick's restrictions, cannot deploy to a docker with requests (and if you could, my 10 hours of trying wasn't enough smh)
    options.add_argument("start-maximized")
    
    print(f'proxy_user: {proxy_user}, proxy_pass: {proxy_pass}, proxy_ip: {proxy_ip}, proxy_port: {proxy_port}')
    proxies_extension = proxies(proxy_user, proxy_pass, proxy_ip, proxy_port)
    options.add_extension(proxies_extension)
    
    
    driver = webdriver.Remote(command_executor=f'http://{selenium_address}:4444/wd/hub', options=options)
    driver.set_page_load_timeout(5)
    driver.get(f"https://api.prizepicks.com/projections?league_id={league}&per_page=250&single_stat=true&in_game=true&state_code=IL&game_mode=pickem")
    while driver.execute_script("return document.readyState") != "complete":
        pass
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(By.XPATH, "/html/body")
    )
    if driver.find_element(By.XPATH, "/html/body") is None:
        return "error, nothing found"
    print(json.loads(driver.find_element(By.XPATH, "/html/body").text))
    data = json.loads(driver.find_element(By.XPATH, "/html/body").text)
    driver.quit()
    for bet in data["data"]:
        for player in data["included"]:
            #return jsonify({"1": player["id"], "2": bet["relationships"]["new_player"]["data"]["id"]})
            if "name" in player["attributes"] and player["id"] == bet["relationships"]["new_player"]["data"]["id"]:
                this_bet = Bet(player["attributes"]["name"], bet["attributes"]["line_score"], player["id"], bet["attributes"]["stat_type"])
                #return jsonify(this_bet.to_dict())
                if league == 9:
                    pp_data_bet_objs_nfl.append(this_bet)
                    pp_data_nfl.append(this_bet.to_dict())
                elif league == 7:
                    pp_data_bet_objs_nba.append(this_bet)
                    pp_data_nba.append(this_bet.to_dict())
                elif league == 8:
                    pp_data_bet_objs_nhl.append(this_bet)
                    pp_data_nhl.append(this_bet.to_dict())
    if league == 9:
        pp_data_bet_objs = pp_data_bet_objs_nfl
        data_ = data_nfl
    elif league == 7:
        pp_data_bet_objs = pp_data_bet_objs_nba
        data_ = data_nba 
    elif league == 8:
        pp_data_bet_objs = pp_data_bet_objs_nhl
        data_ = data_nhl 
    for prize_pick_bet in pp_data_bet_objs:
        #return prize_pick_bet.player_name 
        if prize_pick_bet.player_name in data_.keys():
            if prize_pick_bet.projection_type in data_[prize_pick_bet.player_name].keys(): #I should DEFFO clean this up tbh
                prize_pick_bet.set_info(
                    data_[prize_pick_bet.player_name][prize_pick_bet.projection_type]["l10Rate"],
                    data_[prize_pick_bet.player_name][prize_pick_bet.projection_type]["vsOpp"],
                    data_[prize_pick_bet.player_name][prize_pick_bet.projection_type]["currentSeason"],
                    data_[prize_pick_bet.player_name][prize_pick_bet.projection_type]["under"],
                    data_[prize_pick_bet.player_name][prize_pick_bet.projection_type]["over"],
                    prize_pick_bet.line,
                    data_[prize_pick_bet.player_name][prize_pick_bet.projection_type]["line"],
                )#l10, h2h, in2024
                if league == 9:
                    final_data_nfl.append(prize_pick_bet.to_dict_final())
                    final_data_bet_objs_nfl.append(prize_pick_bet)
                elif league == 7:
                    final_data_nba.append(prize_pick_bet.to_dict_final())
                    final_data_bet_objs_nba.append(prize_pick_bet)   
                elif league == 8: 
                    final_data_nhl.append(prize_pick_bet.to_dict_final())
                    final_data_bet_objs_nhl.append(prize_pick_bet)
    last_updated = datetime.now()
    return jsonify(data)

def get_pp_data_nfl():
    global pp_data_nfl
    return pp_data_nfl
def get_pp_data_bet_objs_nfl():
    global pp_data_bet_objs_nfl
    return pp_data_bet_objs_nfl
def get_final_data_nfl():
    global final_data_nfl
    return final_data_nfl
def get_final_data_bet_objs_nfl():
    global final_data_bet_objs_nfl
    return final_data_bet_objs_nfl

def get_pp_data_nba():
    global pp_data_nba
    return pp_data_nba
def get_pp_data_bet_objs_nba():
    global pp_data_bet_objs_nba
    return pp_data_bet_objs_nba
def get_final_data_nba():
    global final_data_nba
    return final_data_nba
def get_final_data_bet_objs_nba():
    global final_data_bet_objs_nba
    return final_data_bet_objs_nba

def get_pp_data_nhl():
    global pp_data_nhl
    return pp_data_nhl
def get_pp_data_bet_objs_nhl():
    global pp_data_bet_objs_nhl
    return pp_data_bet_objs_nhl
def get_final_data_nhl():
    global final_data_nhl
    return final_data_nhl
def get_final_data_bet_objs_nhl():
    global final_data_bet_objs_nhl
    return final_data_bet_objs_nhl

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

def reset_nba_pp():
    global pp_data_nba
    global pp_data_bet_objs_nba
    global final_data_bet_objs_nba
    global final_data_nba
    pp_data_nba = []
    pp_data_bet_objs_nba = []
    final_data_bet_objs_nba = []
    final_data_nba = []

def reset_nfl_pp():
    global pp_data_nfl
    global pp_data_bet_objs_nfl
    global final_data_bet_objs_nfl
    global final_data_nfl
    pp_data_nfl = []
    pp_data_bet_objs_nfl = []
    final_data_bet_objs_nfl = []
    final_data_nfl = []

def reset_nhl_pp():
    global pp_data_nhl
    global pp_data_bet_objs_nhl
    global final_data_bet_objs_nhl
    global final_data_nhl
    pp_data_nhl = []
    pp_data_bet_objs_nhl = []
    final_data_bet_objs_nhl = []
    final_data_nhl = []
    