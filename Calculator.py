import Testing_math as tm

def Calc():
    checker = "Y"
    counter = 0

    evs = []
    names = []
    pref_rate = []
    opp_rate = []

    while(checker == "Y"):
        names[counter] = str(input("Input the potential leg : "))
        pref_rate[counter] = float(input("Input the preferred rate : "))
        opp_rate[counter] = float(input("Input the opposition rate : "))
        counter += 1
        checker = str(input("Input Y or N : "))

    for i in range(counter + 1):
        evs[i] = tm.ev_calc(pref_rate, opp_rate)

    for i in range(evs):
        print(names[i] + " : " evs[i])

        



