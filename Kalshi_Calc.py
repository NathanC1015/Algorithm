import Kalshi_Functions as KC

"""This is the main script for Kalshi Money"""
#GIMME MONEY BITCHES

# One-time setup (your entry)
entry_mult = float(input("Enter your UNDERDOG entry multiplier (e.g. 2.1): "))
entry_dollars = float(input("Enter your UNDERDOG entry dollars (<= 50): "))

fav_mult_now = 0.1

while True:

    result = KC.tennis_trigger_and_options(entry_mult, entry_dollars, cap=50.0, buffer=0.0)
    KC.print_tennis_plan(result)
    entry_mult = float(input("Enter your UNDERDOG entry multiplier (e.g. 2.1): "))
    entry_dollars = float(input("Enter your UNDERDOG entry dollars (<= 50): "))


    fav_mult_now = float(input("Enter 0 to quit"))
    if fav_mult_now == 0:
        break
