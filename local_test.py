from dice_tools import BasicRoller as DiceRoller

while True:
    roll = input()

    roller = DiceRoller(roll)
    print(roller.sum_all_rolls())
    print(roller.roll_detail_strings())

    # if re.fullmatch(r"((\d+d\d+|\d+)\s*[\-\+]\s*)*\s*(\d+d\d+|\d+)", roll) != None:
    #     dr = DiceRoller(roll)
    #     print(dr.sum_all_rolls())
    # elif re.fullmatch(r"(-max |-min )\s*(\d+d\d+)\s*([\-\+]\s*\d+)?", roll) != None:
    #     dr = DiceRoller( re.sub(r"(-max|-min)\s*", "", roll) )
    #     if roll.find("-min ") == 0:
    #         print(dr.min_all_rolls())
    #     else:
    #         print(dr.max_all_rolls())
    # else:
    #     print("Invalid roll.")
