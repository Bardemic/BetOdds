import requests
import os
from flask import jsonify
from scrapePropsCash import get_data_1

global pp_data
global pp_data_bet_objs
global final_data
pp_data = []
pp_data_bet_objs = [] #Stores the data, but in the Bet class format
final_data = []

def prizepicks_api_fetch():
    global pp_data
    global final_data
    data_1 = get_data_1()
    
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
         "cookie": os.getenv('COOKIE'),
        "referer": "https://www.prizepicks.com/",
    }

    class Bet:
        def __init__(self, player_name, line, new_player_id, projection_type):
            self.player_name = player_name
            self.line = line
            self.new_player_id = new_player_id
            self.og_projection_type = projection_type
            self.l10 = None
            self.h2h = None
            self.in2024 = None
            self.projection_type = "NA"
            match projection_type:
                case "Rush+Rec TDs":
                    self.projection_type = "NA" #check
                case "Sacks":
                    self.projection_type = "sacks"
                case "Longest Reception":
                    self.projection_type = "recLng"
                case "Pass Attempts":
                    self.projection_type = "passAttempts"
                case "Receiving Yards":
                    self.projection_type = "recYards"
                case "FG Made":
                    self.projection_type = "NA" #check
                case "Rush Yards in First 5 Attempts":
                    self.projection_type = "NA" #no chance this is one
                case "Longest Rush":
                    self.projection_type = "rushLng"
                case "Pass Yards":
                    self.projection_type = "passYards"
                case "Rush Yards":
                    self.projection_type = "rushYards"
                case "Pass TDs":
                    self.projection_type = "passTD"
                case "Receptions":
                    self.projection_type = "receptions"
                case "Rush+Rec Yds":
                    self.projection_type = "rushAndRecYards"
                case "Fantasy Score":
                    self.projection_type = "NA"
                case "Field Goal Yards [Combo]":
                    self.projection_type = "NA"
                case "Longest FG Made Yds [Combo]":
                    self.projection_type = "NA"
                case "Rec Targets":
                    self.projection_type = "NA" #few it could be
                case "Pass Completions":
                    self.projection_type = "passCompletions"
                case "INT":
                    self.projection_type = "interceptions" #might be passInt
                case "Pass+Rush Yards":
                    self.projection_type = "passAndRushYards"
                case "Pass Yards [Combo]":
                    self.projection_type = "NA"
                case "Rush Attempts":
                    self.projection_type = "rushAttempts"
                case "FG Made [Combo]":
                    self.projection_type = "NA"
                case "Kicking Points":
                    self.projection_type = "kickingPoints"
                case "Rush Yards [Combo]":
                    self.projection_type = "NA"
                case "Receiving Yards [Combo]":
                    self.projection_type = "NA"
                case "Shortest FG Made Yds [Combo]":
                    self.projection_type = "NA"

        def to_dict(self):
            return { "player_name": self.player_name, "line": self.line, "new_player_id": self.new_player_id, "projection_type": self.projection_type,}
        def to_dict_final(self):
            return { "player_name": self.player_name, "line": self.line, "new_player_id": self.new_player_id, "projection_type": self.projection_type, "l10": self.l10, "H2H": self.h2h, "Current Season": self.in2024,}
        def set_info(self, l10Rate, H2H, in2024):
            self.l10 = l10Rate
            self.h2h = H2H
            self.in2024 = in2024

    try:
        response = requests.get("https://api.prizepicks.com/projections?league_id=9&per_page=250&single_stat=true&in_game=true&state_code=IL&game_mode=pickem", headers=headers)
        print(response)
        response.raise_for_status()
        data = response.json()
        #return data
        #return jsonify(data["data"])
        
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
                if prize_pick_bet.projection_type in data_1[prize_pick_bet.player_name].keys():
                   prize_pick_bet.set_info(data_1[prize_pick_bet.player_name][prize_pick_bet.projection_type]["l10Avg"], data_1[prize_pick_bet.player_name][prize_pick_bet.projection_type]["vsOpp"], data_1[prize_pick_bet.player_name][prize_pick_bet.projection_type]["currentSeason"])#l10, h2h, in2024
                   final_data.append(prize_pick_bet.to_dict_final())
        return jsonify(data)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

def get_pp_data():
    return pp_data
def get_pp_data_bet_objs():
    return pp_data_bet_objs
def get_final_data():
    return final_data