
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

# function to find discrepancy between what might be true probability vs bookmaker odds
def adj_prob(pref_rate,opp_rate):
    # checks if rate we play is negative, converts to implied probability accordingly
    if pref_rate < 0: 
        reciprocal = pref_rate * -1
        implied_pref = reciprocal / (reciprocal+100)
    else:
        implied_pref = 100 / (pref_rate+100)
    # checks if rate against us is negative, converts to implied probability accordingly
    if opp_rate < 0:
        opp_reciprocal = opp_rate * -1
        implied_opp = opp_reciprocal / (opp_reciprocal +100)
    else:
        implied_opp = 100 / (100 + opp_rate)
    # creates adjusted probability
    sum_prob = implied_opp + implied_pref
    adjusted_pref = implied_pref / sum_prob
    adjusted_opp = implied_opp / sum_prob
    return (f"The discrepancy between favorites is adjusted: {adjusted_pref:.2f} - implied {implied_pref:.2f} = {adjusted_pref-implied_pref:.2f} and the discrepancy between the underdogs is adjusted: {adjusted_opp:.2f} - implied: {implied_opp:.2f} = {adjusted_opp-implied_opp:.2f}")

    


    
    
