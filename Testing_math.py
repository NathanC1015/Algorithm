def leg_count():
    legs = float(input("How many legs do you have?:"))
    return legs
def losses():
    losing_bet = float(input("How much would you expect to lose? (How much did you bet):"))
    return float(losing_bet)

def projection():
    bet = float(input("how much did you bet?:"))
    multiplier = float(input("How much will your bet multiply by?:"))
    return float(bet * multiplier)

def Implied_prob_win():
    
    odds = float(input("What are the American odds of winning (negative American):"))
    odds *= -1
    return (f"{float(odds/(odds+100)):.2f}")

def Implied_prob_loss():
    losing_odds = float(input("What are the American odds of losing?:"))
    if losing_odds < 0:
        losing_odds *= -1
        losing_odds = (losing_odds/(losing_odds+100))
    else:
        losing_odds = (100/(losing_odds+100))
    return (losing_odds)

def eV():
    proj = projection()
    impliedWin = float(Implied_prob_win())
    loss = losses()
    impliedLoss = Implied_prob_loss()
    #value = (projection()*Implied_prob_win()) - (losses()*Implied_prob_loss)
    value = (proj*impliedWin) - (loss*impliedLoss)
    return value

print(eV())