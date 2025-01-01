from scrapePrizePicks import get_final_data_bet_objs_nba, get_final_data_bet_objs_nfl
from bet import Bet
global best_nba
global best_nfl
global best_bet_obs_nfl
global best_bet_obs_nba
best_nba = []
best_bet_objs_nba = []
best_nfl = []
best_bet_objs_nfl = []
def bestBets(league):
    global best_nba
    global best_nfl
    global best_bet_objs_nba
    global best_bet_objs_nfl
    if league == 9:
        bets = get_final_data_bet_objs_nfl()
    elif league == 7:
        bets = get_final_data_bet_objs_nba()
    best_nba = []
    best_bet_objs_nba = []
    best_nfl = []
    best_bet_objs_nfl = []

    for bet in bets:
        noneCount = 0
        if bet.l10 == None: noneCount += 1
        if bet.h2h == None: noneCount += 1
        if bet.in2024 == None: noneCount += 1
        if noneCount == 3:
            continue
        if bet.h2h == None and bet.l10 != None and bet.in2024 != None:
            if bet.l10 >= 70 and bet.in2024 >= 70:
                bet.set_avg((bet.l10 + bet.in2024) / 2)
            elif bet.l10 <= 30 and bet.in2024 <= 30:
                bet.set_avg((bet.l10 + bet.in2024) / 2)
        elif noneCount == 0:
            if (bet.l10 >= 64 and bet.in2024 >= 64 and bet.h2h >= 64) or (bet.l10 <= 36 and bet.in2024 <= 36 and bet.h2h <= 36):
                bet.set_avg((bet.l10 + bet.in2024 + bet.h2h) / 3)
            elif (bet.h2h >= 70) and (bet.l10 >= 70 or bet.in2024 >= 70):
                if bet.l10 >= bet.in2024:
                    bet.set_avg((bet.l10 + bet.h2h) / 2)
                else:
                    bet.set_avg((bet.l10 + bet.in2024) / 2)
            elif (bet.h2h <= 30) and (bet.l10 <= 30 or bet.in2024 <= 30):
                if bet.l10 <= bet.in2024:
                    bet.set_avg((bet.l10 + bet.h2h) / 2)
                else:
                    bet.set_avg((bet.in2024 + bet.h2h) / 2)
            
        if bet.avg != None:
            if league == 9:
                best_nfl.append(bet.to_dict_final_with_avg())
                best_bet_objs_nfl.append(bet)
            elif league == 7:
                best_nba.append(bet.to_dict_final_with_avg())
                best_bet_objs_nba.append(bet)
    if league == 9:
        sorted_best = sorted(best_nfl, key=lambda x: abs(50 - x['Average']), reverse=True)
    elif league == 7:
        sorted_best = sorted(best_nba, key=lambda x: abs(50 - x['Average']), reverse=True)
    return sorted_best

        

