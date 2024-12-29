class Bet:
    def __init__(self, player_name, line, new_player_id, projection_type):
        self.player_name = player_name
        self.line = line
        self.new_player_id = new_player_id
        self.og_projection_type = projection_type
        self.l10 = None
        self.h2h = None
        self.in2024 = None
        self.avg = None
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
    def to_dict_final_with_avg(self):
        return { "player_name": self.player_name, "line": self.line, "new_player_id": self.new_player_id, "projection_type": self.projection_type, "l10": self.l10, "H2H": self.h2h, "Current Season": self.in2024, "Average": self.avg}
    def set_info(self, l10Rate, H2H, in2024):
        self.l10 = l10Rate
        self.h2h = H2H
        self.in2024 = in2024
    def set_avg(self, avg):
        self.avg = avg