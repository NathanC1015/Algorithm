

'''
 This function is intended to be used for removing bookie's margins from the odds to find what they truly believe is the odds of a certain line hitting.
These lines are subject to change, and we should only be using the function to supplement our research. 
For example, (I think) if we find Pinnacle's adjusted odds by running the function once and take Caesar's adjusted odds by running the function another time. Pinnacle could give us an adjusted probability of 60% and Caesar's to give us 58%.
Because of this, there is value to be made from betting on Caesar's, assuming that we can trust Pinnacle for being marked to true odds.
This function returns a string to make for easy reading, but appending to a list will be very aids.
REMEMBER: USE THIS FUNCTION TWICE TO COMPARE PINNACLE'S ODDS VS. ANY OTHER BOOK's ODDS.
'''
import random
from itertools import combinations


def adj_probWin():
    hit, noHit = player_lines()
    hitOdds, noHitOdds = [], []
    
    for pref_rate in hit.values():
    # checks if rate we play is negative, converts to implied probability accordingly
        if pref_rate < 0: 
            reciprocal = pref_rate * -1
            implied_pref = reciprocal / (reciprocal+100)
            hitOdds.append(implied_pref)
        else:
            implied_pref = 100 / (pref_rate+100)
            hitOdds.append(implied_pref)
            
            
    for opp_rate in noHit.values():
        
        # checks if rate against us is negative, converts to implied probability accordingly
        if opp_rate < 0:
            opp_reciprocal = opp_rate * -1
            implied_opp = opp_reciprocal / (opp_reciprocal +100)
            noHitOdds.append(implied_opp)
        else:
            implied_opp = 100 / (100 + opp_rate)
            noHitOdds.append(implied_opp)
    # creates adjusted probability
    for index in range(len(hitOdds)):
        sum_prob = noHitOdds[index] + hitOdds[index]
        noHitOdds[index] = noHitOdds[index] / sum_prob
        hitOdds[index] = hitOdds[index] / sum_prob
    
    
    hitLine = [] 
    for key in hit:
        hitLine.append(key)
    
    # now have 2 lists of adjusted probabilities, nohitodds and hitodds
    i = 0
    for key in hit:
        hit[key] = hitOdds[i]
        i += 1
    i = 0
    for key in noHit:
        noHit[key] = noHitOdds[i]
        i += 1
        
    prodList, comboList, hitList = [], [], []
    for combo in combinations(hitOdds, 3): # change 3 according to how many to hit
        first, second, third = combo
        comboList.append(combo)
        prod = first * second * third
        prodList.append(prod)
        print(prodList)
        
    for combo in combinations(hitLine, 3):
        hitList.append(combo)
    
    top10 = []
    for i in range(10):
        bestOdd = max(prodList)
        top10.append(bestOdd)
        bestIndex = prodList.index(bestOdd) # index of best probability
        print(bestOdd)
        print(hitList[bestIndex])
        print()
        prodList.remove(bestOdd)
        del hitList[bestIndex]
        if len(prodList) == 0:
            break

        

    return top10
    #(f"The discrepancy between favorites is adjusted: {adjusted_pref:.2f} - implied {implied_pref:.2f} = {adjusted_pref-implied_pref:.2f} and the discrepancy between the underdogs is adjusted: {adjusted_opp:.2f} - implied: {implied_opp:.2f} = {adjusted_opp-implied_opp:.2f}")

# this function will take user inputs of statlines
def player_lines():
    odds = {}
    odds_against = {}
    pref_rate = (input("What is the line you're hitting?: "))
    opp_rate = (input("What is the line against you?: "))
    # while loop to take in player lines and odds
    while pref_rate != '':
        line_against = opp_rate[:-4]
        chance_against = opp_rate[-4:]
        odds_against[line_against] = float(chance_against)
        line = pref_rate[:-5].strip()
        chance = pref_rate[-4:].strip()
        odds[line] = float(chance)
        pref_rate = (input("What is the line you're hitting?: "))
        if pref_rate == '':
            break
        opp_rate = (input("What is the line against you?: "))
        
    return odds, odds_against


multiplier = {3.0:6, 5.0:20}


def ev():
    legs = float(input("How many legs do you want?: "))
    bet_amt = float(input("How much are you betting?: "))
    winning_odds = adj_probWin()# equal to top10 probabilities
    losing = 1
    
    while bet_amt < 0:
        print("You have entered an invalid number!")
        bet_amt = float(input("How much are you betting?: "))
    payout =  multiplier[legs]* bet_amt
    # for i in range(int(legs)):
    #     winning_odds.append(adj_probWin()[0])
    # for x in winning_odds:
    #     winning *= x
    for elem in range(len(winning_odds)):
        losing -= winning_odds[elem]
        ev = (payout * winning_odds[elem]) - (bet_amt * losing)
        losing = 1
        if ev < 0:
            print(f"For your bet, ${bet_amt}, you expect to lose ${abs(ev):.2f} and your odds of winning are {winning_odds[elem]*100:.2f}%")
        else:
            print(f"For your bet, ${bet_amt}, you expect to gain ${ev:.2f} and your odds of winning are {winning_odds[elem]*100:.2f}%")
    return []
    

def luck_gen():
    luck = random.randint(0,1)
    return luck
    
    

