class Bet:
    def __init__(self, player_name, line, new_player_id, projection_type):
        self.player_name = player_name
        self.line = line
        self.new_player_id = new_player_id
        self.og_projection_type = projection_type
        self.over =  None
        self.under = None
        self.l10 = None
        self.h2h = None
        self.in2024 = None
        self.avg = None
        self.pc_line = None
        self.pp_line = None
        self.projection_type = projection_map.get(projection_type, "NA")



    def to_dict(self):
        return {
            "player_name": self.player_name,
            "line": self.line,
            "new_player_id":self.new_player_id,
            "projection_type": self.projection_type,
        }
    def to_dict_final(self):
        return {
            "player_name": self.player_name,
            "line": self.line,
            "new_player_id": self.new_player_id,
            "projection_type": self.projection_type,
            "l10": self.l10,
            "H2H": self.h2h,
            "Current Season": self.in2024
        }
    def to_dict_final_with_avg(self):
        return {
            "player_name": self.player_name,
            "line": self.line, 
            "new_player_id": self.new_player_id, 
            "projection_type": self.projection_type, 
            "l10": self.l10, 
            "H2H": self.h2h, 
            "Current Season": self.in2024,
            "Average": self.avg,
            "under": self.under,
            "over": self.over,
            "pp_line": self.pp_line,
            "pc_line": self.pc_line
            }
    def set_info(self, l10Rate, H2H, in2024, under, over, line_pp, line_pc):
        self.l10 = l10Rate
        self.h2h = H2H
        self.in2024 = in2024
        self.under = under
        self.over = over
        self.pp_line = line_pp
        self.pc_line = line_pc
    def set_avg(self, avg):
        self.avg = avg

projection_map = {
    #NFL
    "Rush+Rec TDs": "NA",
    "Sacks": "sacks",
    "Longest Reception": "recLng",
    "Pass Attempts": "passAttempts",
    "Receiving Yards": "recYards",
    "FG Made": "NA",
    "Rush Yards in First 5 Attempts": "NA",
    "Longest Rush": "rushLng",
    "Pass Yards": "passYards",
    "Rush Yards": "rushYards",
    "Pass TDs": "passTD",
    "Receptions": "receptions",
    "Rush+Rec Yds": "rushAndRecYards",
    "Fantasy Score": "NA",
    "Field Goal Yards [Combo]": "NA",
    "Longest FG Made Yds [Combo]": "NA",
    "Rec Targets": "NA",
    "Pass Completions": "passCompletions",
    "INT": "interceptions",
    "Pass+Rush Yards": "passAndRushYards",
    "Pass Yards [Combo]": "NA",
    "Rush Attempts": "rushAttempts",
    "FG Made [Combo]": "NA",
    "Kicking Points": "kickingPoints",
    "Rush Yards [Combo]": "NA",
    "Receiving Yards [Combo]": "NA",
    "Shortest FG Made Yds [Combo]": "NA",
    # NBA
    "Pts+Asts": "pointsAssists",
    "Assists": "assists",
    "Blocked Shots": "blocks",
    "Pts+Rebs": "pointsRebounds",
    "Pts+Rebs+Asts": "pointsReboundsAssists",
    "Blks+Stls": "stealsAndBlocks",
    "Points": "points",
    "Rebounds": "rebounds",
    "Rebs+Asts": "reboundsAssists",
    "Steals": "steals",
    "3-PT Made": "fg3PtMade",
    "Turnovers": "turnovers",
}