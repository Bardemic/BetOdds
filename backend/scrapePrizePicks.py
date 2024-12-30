import requests
import os
from flask import jsonify
from scrapePropsCash import get_data_1
from bet import Bet

global pp_data
global pp_data_bet_objs
global final_data_bet_objs
global final_data
pp_data = []
pp_data_bet_objs = [] #Stores the data, but in the Bet class format
final_data = []
final_data_bet_objs = []

def prizepicks_api_fetch():
    global pp_data
    global pp_data_bet_objs
    global final_data
    global final_data_bet_objs
    data_1 = get_data_1()
    
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
         "cookie": os.getenv('COOKIE'),
        "referer": "https://www.prizepicks.com/",
    }


    try:
        response = requests.get("https://api.prizepicks.com/projections?league_id=9&per_page=250&single_stat=true&in_game=true&state_code=IL&game_mode=pickem", headers=headers)
        print(response)
        response.raise_for_status()
        data = response.json()
        #return data
        #return jsonify(data["data"])
        
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
        return jsonify(data)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

def get_pp_data():
    return pp_data
def get_pp_data_bet_objs():
    return pp_data_bet_objs
def get_final_data():
    return final_data
def get_final_data_bet_objs():
    global final_data_bet_objs
    return final_data_bet_objs