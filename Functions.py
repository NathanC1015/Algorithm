

'''
 This function is intended to be used for removing bookie's margins from the odds to find what they truly believe is the odds of a certain line hitting.
These lines are subject to change, and we should only be using the function to supplement our research. 
For example, (I think) if we find Pinnacle's adjusted odds by running the function once and take Caesar's adjusted odds by running the function another time. Pinnacle could give us an adjusted probability of 60% and Caesar's to give us 58%.
Because of this, there is value to be made from betting on Caesar's, assuming that we can trust Pinnacle for being marked to true odds.
This function returns a string to make for easy reading, but appending to a list will be very aids.
REMEMBER: USE THIS FUNCTION TWICE TO COMPARE PINNACLE'S ODDS VS. ANY OTHER BOOK's ODDS.
'''
def adj_probWin():
    pref_rate = float(input("What are your odds?: "))
    opp_rate = float(input("What are the odds against you?: "))
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
    adjusted_opp = implied_opp / sum_prob
    adjusted_pref = implied_pref / sum_prob

    return adjusted_pref, adjusted_opp
    #(f"The discrepancy between favorites is adjusted: {adjusted_pref:.2f} - implied {implied_pref:.2f} = {adjusted_pref-implied_pref:.2f} and the discrepancy between the underdogs is adjusted: {adjusted_opp:.2f} - implied: {implied_opp:.2f} = {adjusted_opp-implied_opp:.2f}")



def parlay_odds():
    global legs
    legs = float(input("How many legs do you want?: "))
    return legs

multiplier = {3.0:10, 5.0:20}


def ev():
    parlay_odds()
    winning = 1
    winning_odds = []
    losing = 1
    bet_amt = float(input("How much are you betting?: "))
    while bet_amt < 0:
        print("You have entered an invalid number!")
        bet_amt = float(input("How much are you betting?: "))
    payout =  multiplier[legs]* bet_amt
    for i in range(int(legs)):
        winning_odds.append(adj_probWin()[0])
    for x in winning_odds:
        winning *= x
    losing -= winning
    ev = (payout * winning) - (bet_amt * losing)
    return (f"For your bet, ${bet_amt}, you expect to gain ${ev:.2f}")




        
    
    
    
