from scrapePrizePicks import get_final_data_bet_objs
from bet import Bet
global best
global best_bet_objs
best = []
best_bet_objs = []
def bestBets():
    bets = get_final_data_bet_objs()
    best = []
    best_bet_objs = []
    for bet in bets:
        noneCount = 0
        if bet.l10 == None: noneCount += 1
        if bet.h2h == None: noneCount += 1
        if bet.in2024 == None: noneCount += 1
        if noneCount == 3:
            continue
        if bet.h2h == None and bet.l10 != None and bet.in2024 != None:
            if bet.l10 >= 65 and bet.in2024 >= 65:
                bet.set_avg((bet.l10 + bet.in2024) / 2)
            elif bet.l10 <= 35 and bet.in2024 <= 35:
                bet.set_avg((bet.l10 + bet.in2024) / 2)
        elif noneCount == 0:
            if (bet.l10 >= 60 and bet.in2024 >= 60 and bet.h2h >= 60) or (bet.l10 <= 40 and bet.in2024 <= 40 and bet.h2h <= 40):
                bet.set_avg((bet.l10 + bet.in2024 + bet.h2h) / 3)
            elif (bet.h2h >= 65) and (bet.l10 >= 65 or bet.in2024 >= 65):
                if bet.l10 >= bet.in2024:
                    bet.set_avg((bet.l10 + bet.h2h) / 2)
                else:
                    bet.set_avg((bet.l10 + bet.in2024) / 2)
            elif (bet.h2h <= 35) and (bet.l10 <= 35 or bet.in2024 <= 35):
                if bet.l10 <= bet.in2024:
                    bet.set_avg((bet.l10 + bet.h2h) / 2)
                else:
                    bet.set_avg((bet.in2024 + bet.h2h) / 2)
            
        if bet.avg != None:
            best.append(bet.to_dict_final_with_avg())
            best_bet_objs.append(bet)
    sorted_best = sorted(best, key=lambda x: abs(50 - x['Average']))
    return sorted_best

        

