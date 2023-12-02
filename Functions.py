
def ev_calc(pref_rate,opp_rate,bet_amt):
    if pref_rate < 0:
        pref_odds1 = pref_rate *-1 
        pref_odds = pref_rate*-1
        pref_odds = pref_odds/(pref_odds+100)
        payout = bet_amt * (100/pref_odds1)
        winning = payout * pref_odds 
    else:
        pref_odds = 100 / (pref_rate+100)
        payout = bet_amt * (pref_rate / 100)
        winning = payout * pref_odds
    if opp_rate < 0: 
        opp_odds1 = opp_rate *-1
        opp_odds = opp_rate * - 1
        opp_odds = opp_odds / (opp_odds+100)
        losses = bet_amt * opp_odds


    else:
        opp_odds = 100 / (opp_rate+100)
        losses = bet_amt * opp_odds
    ev = winning - losses
    return ev



    
    
